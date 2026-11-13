"""Load PolyFEM contact source JSON into generated-style config objects."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import polyfem


class SourcePayloadConfig:
    """Generated-example fallback for source JSON shapes not yet in generated API."""

    def __init__(
        self,
        payload: dict[str, Any],
        *,
        source_json: Path,
        fallback_reason: str,
    ) -> None:
        self.source_json = Path(source_json)
        self.fallback_reason = fallback_reason
        self._payload = copy.deepcopy(payload)

    def as_dict(self) -> dict[str, Any]:
        return copy.deepcopy(self._payload)


def load_polyfem_config(source_json: Path) -> Any:
    payload = load_contact_source_payload(source_json)
    try:
        return polyfem.config(**payload)
    except TypeError as exc:
        return SourcePayloadConfig(
            payload,
            source_json=source_json,
            fallback_reason=str(exc),
        )


def load_contact_source_payload(source_json: Path) -> dict[str, Any]:
    source_json = Path(source_json).resolve()
    payload = _load_contact_source_payload(source_json)
    _resolve_mesh_paths(payload, source_json.parent)
    _normalize_solver_fallbacks(payload)
    _normalize_generated_mesh_payloads(payload, source_json.parent)
    return payload


def _load_contact_source_payload(source_json: Path) -> dict[str, Any]:
    with source_json.open(encoding="utf-8") as f:
        source = json.load(f)

    if not isinstance(source, dict):
        raise TypeError(f"source JSON must contain an object: {source_json}")

    source.pop("tests", None)
    source.pop("default_params", None)
    common_ref = source.pop("common", None)
    patch = source.pop("patch", None)

    if common_ref is None:
        payload = source
    else:
        common_path = (source_json.parent / common_ref).resolve()
        payload = _deep_merge(_load_contact_source_payload(common_path), source)

    if patch:
        payload = _apply_json_patch(payload, patch)

    return payload


def _deep_merge(base: Any, override: Any) -> Any:
    if isinstance(base, dict) and isinstance(override, dict):
        merged = copy.deepcopy(base)
        for key, value in override.items():
            merged[key] = _deep_merge(merged[key], value) if key in merged else copy.deepcopy(value)
        return merged
    return copy.deepcopy(override)


def _apply_json_patch(payload: dict[str, Any], patch: list[dict[str, Any]]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    for item in patch:
        if item.get("op") != "replace":
            raise ValueError(f"unsupported JSON patch op: {item!r}")
        _replace_json_pointer(result, item["path"], item.get("value"))
    return result


def _replace_json_pointer(payload: Any, pointer: str, value: Any) -> None:
    target = payload
    tokens = _json_pointer_tokens(pointer)
    for token in tokens[:-1]:
        target = target[int(token)] if isinstance(target, list) else target[token]

    last = tokens[-1]
    if isinstance(target, list):
        target[int(last)] = copy.deepcopy(value)
    else:
        target[last] = copy.deepcopy(value)


def _json_pointer_tokens(pointer: str) -> list[str]:
    if not pointer.startswith("/"):
        raise ValueError(f"JSON patch path must start with '/': {pointer!r}")
    return [
        token.replace("~1", "/").replace("~0", "~")
        for token in pointer[1:].split("/")
    ]


def _resolve_mesh_paths(value: Any, source_dir: Path) -> None:
    if isinstance(value, list):
        for item in value:
            _resolve_mesh_paths(item, source_dir)
    elif isinstance(value, dict):
        for key in ("mesh", "linear_map"):
            path_value = value.get(key)
            if isinstance(path_value, str):
                value[key] = str((source_dir / path_value).resolve())
        for child in value.values():
            _resolve_mesh_paths(child, source_dir)


def _normalize_solver_fallbacks(config: dict[str, Any]) -> None:
    solver = config.get("solver")
    if not isinstance(solver, dict):
        return
    linear = solver.get("linear")
    if not isinstance(linear, dict):
        return
    solver_name = linear.get("solver")
    if isinstance(solver_name, list):
        linear["solver"] = solver_name[0]


def _normalize_generated_mesh_payloads(config: dict[str, Any], source_dir: Path) -> None:
    geometry = config.get("geometry")
    if not isinstance(geometry, list):
        return

    for item in geometry:
        if not isinstance(item, dict) or "mesh" not in item:
            continue
        item.setdefault("type", "mesh")
        _normalize_file_selection(item, "volume_selection", source_dir)
        _normalize_file_selection(item, "surface_selection", source_dir)

        transformation = item.get("transformation")
        if not isinstance(transformation, dict):
            continue
        for field in ("rotation", "scale"):
            if isinstance(transformation.get(field), (int, float)):
                transformation[field] = [float(transformation[field])]


def _normalize_file_selection(item: dict[str, Any], field: str, source_dir: Path) -> None:
    selection = item.get(field)
    if isinstance(selection, str):
        item[field] = {"file": _resolve_source_file_path(selection, source_dir)}
    elif isinstance(selection, dict):
        file_path = selection.get("file")
        if isinstance(file_path, str):
            selection["file"] = _resolve_source_file_path(file_path, source_dir)


def _resolve_source_file_path(path_value: str, source_dir: Path) -> str:
    path = Path(path_value)
    if path.is_absolute():
        return path_value
    return str((source_dir / path).resolve())
