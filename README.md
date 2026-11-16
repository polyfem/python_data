# PolyFEM Python Data

This repository stores runnable Python examples for `polyfem-python`.

It is intended to be checked out as the `examples/` submodule inside
`polyfem-python`:

```bash
git submodule update --init --recursive examples
```

## Layout

- `quickstart/`: small, self-contained examples for the public API.
- `classic_example/2D/`: 2D generated-API examples.
- `classic_example/3D/`: 3D generated-API examples.

## Quick start

Install `polyfempy` first, then run these commands from this repository:

```sh
python quickstart/static_elasticity.py
python quickstart/transient_elasticity.py
```

Both examples create a small square mesh and need no external data files.
They use `Eigen::SimplicialLDLT`, which does not require Pardiso. The transient
example runs five time steps and writes to `results/transient_square`.

## Classic example dependencies

These examples import:

```python
import polyfem
from polyfempy import solve
```

They also read source JSON files and meshes from `polyfem-data/contact`.
By default, the helper scripts look for a sibling `polyfem-data` checkout:

- inside `polyfem-python/examples`, this resolves to `polyfem-python/polyfem-data`;
- in a standalone `python_data` checkout, this resolves to `polyfem-data` next
  to `python_data`.

To use a different location, set:

```bash
export POLYFEM_DATA_ROOT=/path/to/polyfem-data
```

On PowerShell:

```powershell
$env:POLYFEM_DATA_ROOT = "C:\path\to\polyfem-data"
```

## Run

First generate and install the parent `polyfem-python` package according to its
`BUILD.md`, then use that same Python environment here. Cloning this repository
does not install the compiled solver. The parent README's small square example
is the first installation check; these contact cases are larger reference models.

Most cases explicitly select `Eigen::PardisoLDLT`, which requires a backend build
with that solver available. The parent's regression diagnostic substitutes a
portable solver and follows the reference `tests.time_steps`; it is not identical
to running a full example directly.

From this repository root:

```bash
python classic_example/2D/contact_2d_golf_ball_generated_api.py
```

From the parent `polyfem-python` repository root:

```bash
python examples/classic_example/2D/contact_2d_golf_ball_generated_api.py
```

Outputs follow each example's explicit `output.directory`, normally
`results/2D/...` or `results/3D/...`, relative to the directory where you run it.
Repeated runs use that same directory. The repository ignores `results/` so
simulation output is kept out of source control. Reference JSON inputs remain
tracked in the data repository.
