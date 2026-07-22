#!/usr/bin/env python3
"""Classic 3D large-ratios sphere-mat example using generated_api.

Mirrors ``polyfem-data/contact/examples/3D/large-ratios/sphere-mat.json``.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

EXAMPLE_DIR = Path(__file__).resolve().parent
if str(EXAMPLE_DIR) not in sys.path:
    sys.path.insert(0, str(EXAMPLE_DIR))

from _contact_3d_common import (  # noqa: E402
    CONTACT_EXAMPLES_DIR,
    MESHES_DIR,
    config_for_workspace_from,
    polyfem,
    run_solve,
)


SOURCE_JSON = CONTACT_EXAMPLES_DIR / "3D" / "large-ratios" / "sphere-mat.json"

model = polyfem.model()

sphere_material = polyfem.neo_hookean(E=100000000.0, nu=0.4, rho=2000)
mat_material = polyfem.neo_hookean(E=1000000.0, nu=0.4, rho=1000)

sphere = model.mesh(
    mesh=str(MESHES_DIR / "3D" / "simple" / "sphere" / "sphere1K.msh"),
    transformation=polyfem.transformation(
        translation=[0, 1, 0],
        rotation=[90, 0, 45],
        rotation_mode="zyx",
    ),
)
sphere.material(sphere_material)

mat = model.mesh(
    mesh=str(MESHES_DIR / "3D" / "simple" / "mat" / "mat40x40.msh"),
    transformation=polyfem.transformation(scale=2),
)
mat.material(mat_material)
mat.surface_axis(axis="-x", position=-1).dirichlet(value=["-min(t,0.28)", 0, 0])
mat.surface_axis(axis="x", position=1).dirichlet(value=["min(t,0.28)", 0, 0])

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
    rhs=[0, 9.81, 0],
    time_tend=2.5,
    time_dt=0.01,
    contact=polyfem.contact(enabled=True, dhat=0.001),
    solver=solver,
    output=output,
)


def config_for_workspace(workspace: Path) -> Any:
    return config_for_workspace_from(polyfem_config, workspace)


def main() -> int:
    return run_solve(polyfem_config, "contact_3d_large_ratios_sphere_mat_generated_api")


if __name__ == "__main__":
    raise SystemExit(main())
