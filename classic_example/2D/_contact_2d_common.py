"""Runtime helpers shared by classic 2D generated-api examples."""

from __future__ import annotations

import copy
import os
import time
from pathlib import Path
from typing import Any

from polyfempy.runtime import solve
from polyfempy.generated_api import generated_api as polyfem


REPO_ROOT = Path(__file__).resolve().parents[3]
CLASSIC_2D_DIR = Path(__file__).resolve().parent
POLYFEM_DATA_ROOT = Path(
    os.environ.get("POLYFEM_DATA_ROOT", REPO_ROOT / "polyfem-data")
).expanduser().resolve()
POLYFEM_DATA_CONTACT = POLYFEM_DATA_ROOT / "contact"
DATA_CONTACT = POLYFEM_DATA_CONTACT
CONTACT_EXAMPLES_DIR = POLYFEM_DATA_CONTACT / "examples"
MESHES_DIR = POLYFEM_DATA_CONTACT / "meshes"
RUNS_DIR = CLASSIC_2D_DIR / "2D_examples_outputs"


def make_timestamped_workspace(base_dir: Path | str, tag: str) -> Path:
    workspace_root = Path(base_dir).resolve()
    workspace = workspace_root / f"{tag}_{int(time.time())}"
    workspace.mkdir(parents=True, exist_ok=True)
    return workspace.resolve()


def config_for_workspace_from(polyfem_config: Any, workspace: Path) -> Any:
    cfg = copy.deepcopy(polyfem_config)
    cfg.output.directory = str(workspace)
    if cfg.output.log is not None:
        cfg.output.log.path = str(workspace / "polyfem.log")
    return cfg


def run_solve(polyfem_config: Any, example_name: str) -> int:
    workspace = make_timestamped_workspace(RUNS_DIR, example_name)
    solve(cfg=config_for_workspace_from(polyfem_config, workspace))
    return 0
