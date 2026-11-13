"""Runtime helpers shared by classic 2D generated-api examples."""

from __future__ import annotations

import os
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
CLASSIC_EXAMPLES_DIR = Path(__file__).resolve().parents[1]
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
CONTACT_EXAMPLES_DIR = POLYFEM_DATA_CONTACT / "examples"
MESHES_DIR = POLYFEM_DATA_CONTACT / "meshes"
