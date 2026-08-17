"""Runtime helpers shared by classic 3D generated-api examples."""

from __future__ import annotations

import copy
import os
import sys
import time
from pathlib import Path
from typing import Any

from polyfempy.generated_api import generated_api as polyfem
from polyfempy.runtime import solve


REPO_ROOT = Path(__file__).resolve().parents[3]
CLASSIC_EXAMPLES_DIR = Path(__file__).resolve().parents[1]
CLASSIC_3D_DIR = Path(__file__).resolve().parent
if str(CLASSIC_EXAMPLES_DIR) not in sys.path:
    sys.path.insert(0, str(CLASSIC_EXAMPLES_DIR))

from _contact_source_loader import (  # noqa: E402
    SourcePayloadConfig,
    load_polyfem_config,
)

POLYFEM_DATA_ROOT = Path(
    os.environ.get("POLYFEM_DATA_ROOT", REPO_ROOT / "polyfem-data")
).expanduser().resolve()
POLYFEM_DATA_CONTACT = POLYFEM_DATA_ROOT / "contact"
DATA_CONTACT = POLYFEM_DATA_CONTACT
MESHES_DIR = POLYFEM_DATA_CONTACT / "meshes"
CONTACT_EXAMPLES_DIR = POLYFEM_DATA_CONTACT / "examples"
RUNS_DIR = CLASSIC_3D_DIR / "3D_examples_outputs"


def make_timestamped_workspace(base_dir: Path | str, tag: str) -> Path:
    workspace_root = Path(base_dir).resolve()
    workspace = workspace_root / f"{tag}_{int(time.time())}"
    workspace.mkdir(parents=True, exist_ok=True)
    return workspace.resolve()


def config_for_workspace_from(polyfem_config: Any, workspace: Path) -> Any:
    cfg = copy.deepcopy(polyfem_config)
    if isinstance(cfg, SourcePayloadConfig):
        return cfg.with_output_workspace(workspace)
    if cfg.output is not None:
        cfg.output.directory = str(workspace)
        if cfg.output.log is not None:
            cfg.output.log.path = str(workspace / "polyfem.log")
    return cfg


def run_solve(polyfem_config: Any, example_name: str) -> int:
    workspace = make_timestamped_workspace(RUNS_DIR, example_name)
    solve(cfg=config_for_workspace_from(polyfem_config, workspace))
    return 0
