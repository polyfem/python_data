#!/usr/bin/env python3
"""Classic 2D friction rollers example using generated_api.

Mirrors ``polyfem-data/contact/examples/2D/friction/circle-rollers.json``.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

EXAMPLE_DIR = Path(__file__).resolve().parent
if str(EXAMPLE_DIR) not in sys.path:
    sys.path.insert(0, str(EXAMPLE_DIR))

from _contact_2d_common import (  # noqa: E402
    CONTACT_EXAMPLES_DIR,
    MESHES_DIR,
    config_for_workspace_from,
    polyfem,
    run_solve,
)


SOURCE_JSON = CONTACT_EXAMPLES_DIR / "2D" / "friction" / "circle-rollers.json"

model = polyfem.model()

rubber = polyfem.neo_hookean(E=10000, nu=0.4, rho=1000)
steel = polyfem.neo_hookean(E=200000000000.0, nu=0.3, rho=7750)

center = model.mesh(
    mesh=str(MESHES_DIR / "2D" / "simple" / "circle" / "circle2K.obj"),
    enabled=True,
    transformation=polyfem.transformation(translation=[0, 0.5], scale=2),
)
center.material(rubber)

left_roller = model.mesh(
    mesh=str(MESHES_DIR / "2D" / "simple" / "circle" / "circle14.obj"),
    transformation=polyfem.transformation(translation=[-0.5, -1], scale=0.8),
)
left_roller.material(steel)
left_roller.surface_all(id=1).dirichlet(
    value=[
        "rotate_2D_x(x + 0.5, y + 1, -t * pi / 2) - (x + 0.5)",
        "rotate_2D_y(x + 0.5, y + 1, -t * pi / 2) - (y + 1)",
    ],
)

right_roller = model.mesh(
    mesh=str(MESHES_DIR / "2D" / "simple" / "circle" / "circle14.obj"),
    enabled=True,
    transformation=polyfem.transformation(translation=[0.5, -1], scale=0.8),
)
right_roller.material(steel)
right_roller.surface_all(id=2).dirichlet(
    value=[
        "rotate_2D_x(x - 0.5, y + 1, t * pi / 2) - (x - 0.5)",
        "rotate_2D_y(x - 0.5, y + 1, t * pi / 2) - (y + 1)",
    ],
)

ground = model.mesh(
    mesh=str(MESHES_DIR / "2D" / "simple" / "square.obj"),
    enabled=True,
    transformation=polyfem.transformation(
        translation=[0, -4.01],
        scale=[8, 0.02],
    ),
)
ground.material(steel)
ground.surface_all(id=3).dirichlet(value=[0, 0])

solver = polyfem.solver(
    linear=polyfem.linear(solver="Eigen::PardisoLDLT"),
    nonlinear=polyfem.nonlinear(
        iterations_per_strategy=1,
        line_search=polyfem.line_search(method="RobustArmijo"),
        solver="Newton",
    ),
    contact=polyfem.solver_contact(friction_iterations=1),
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
        save_solve_sequence_debug=True,
        save_time_sequence=True,
    ),
)

polyfem_config = model.config(
    rhs=[0, 9.81],
    time_tend=10,
    time_dt=0.01,
    contact=polyfem.contact(
        enabled=True,
        dhat=0.001,
        epsv=0.004,
        friction_coefficient=0.5,
    ),
    solver=solver,
    output=output,
)


def config_for_workspace(workspace: Path) -> Any:
    return config_for_workspace_from(polyfem_config, workspace)


def main() -> int:
    return run_solve(polyfem_config, "contact_2d_friction_circle_rollers_generated_api")


if __name__ == "__main__":
    raise SystemExit(main())
