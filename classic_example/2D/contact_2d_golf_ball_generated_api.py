#!/usr/bin/env python3
"""Classic 2D golf-ball contact example using generated_api.

Mirrors ``polyfem-data/contact/examples/2D/golf-ball.json``.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import polyfem

EXAMPLE_DIR = Path(__file__).resolve().parent
if str(EXAMPLE_DIR) not in sys.path:
    sys.path.insert(0, str(EXAMPLE_DIR))

from _contact_2d_common import (  # noqa: E402
    CONTACT_EXAMPLES_DIR,
    MESHES_DIR,
    config_for_workspace_from,
    run_solve,
)


SOURCE_JSON = CONTACT_EXAMPLES_DIR / "2D" / "golf-ball.json"

model = polyfem.model()

rubber = polyfem.neo_hookean(E=10000000.0, nu=0.45, rho=1150)
steel = polyfem.neo_hookean(E=200000000000.0, nu=0.3, rho=7750)

ball = model.mesh(
    mesh=str(MESHES_DIR / "2D" / "simple" / "circle" / "circle9K.obj"),
    transformation=polyfem.transformation(scale=0.04),
)
ball.material(rubber)
ball.velocity(polyfem.velocity_item(value=[67, 0]))

wall = model.mesh(
    mesh=str(MESHES_DIR / "2D" / "simple" / "square.obj"),
    transformation=polyfem.transformation(
        translation=[0.105, 0],
        dimensions=[0.01, 0.4],
    ),
)
wall.material(steel)
wall.surface_all(id=1).dirichlet(value=[0, 0])

solver = polyfem.solver(
    linear=polyfem.linear(solver="Eigen::PardisoLDLT"),
    nonlinear=polyfem.nonlinear(
        iterations_per_strategy=1,
        line_search=polyfem.line_search(method="RobustArmijo"),
        solver="Newton",
    ),
    advanced=polyfem.solver_advanced(lump_mass_matrix=True),
)

output = polyfem.output(
    json="sim.json",
    paraview=polyfem.output_paraview(
        file_name="sim.pvd",
        options=polyfem.options(
            material=True,
            body_ids=True,
            tensor_values=False,
            discretization_order=False,
            nodes=False,
        ),
        vismesh_rel_area=10000000,
    ),
    advanced=polyfem.output_advanced(
        save_solve_sequence_debug=False,
        save_time_sequence=True,
    ),
)

polyfem_config = model.config(
    rhs=[0, 0],
    time_tend=0.004,
    time_dt=2e-05,
    contact=polyfem.contact(enabled=True, dhat=6.92820323e-05),
    solver=solver,
    output=output,
)


def config_for_workspace(workspace: Path) -> Any:
    return config_for_workspace_from(polyfem_config, workspace)


def main() -> int:
    return run_solve(polyfem_config, "contact_2d_golf_ball_generated_api")


if __name__ == "__main__":
    raise SystemExit(main())
