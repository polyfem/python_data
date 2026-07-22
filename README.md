# PolyFEM Python Data

This repository stores runnable Python examples for `polyfem-python`.

It is intended to be checked out as the `examples/` submodule inside
`polyfem-python`:

```bash
git submodule update --init --recursive examples
```

## Layout

- `classic_example/2D/`: 2D generated-API examples.
- `classic_example/3D/`: 3D generated-API examples.

## Runtime Dependencies

These examples import:

```python
from polyfempy.runtime import solve
from polyfempy.generated_api import generated_api as polyfem
```

They also read source JSON files and meshes from `polyfem-data/contact`.
By default, the helper scripts look for `polyfem-data` next to the repository
root used by the checkout. To use a different location, set:

```bash
export POLYFEM_DATA_ROOT=/path/to/polyfem-data
```

On PowerShell:

```powershell
$env:POLYFEM_DATA_ROOT = "C:\path\to\polyfem-data"
```

## Run

From the repository root:

```bash
python classic_example/2D/contact_2d_golf_ball_generated_api.py
```

Example outputs are written under the corresponding `*_examples_outputs/`
directory and are ignored by Git.
