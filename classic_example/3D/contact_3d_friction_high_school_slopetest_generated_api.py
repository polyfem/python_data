#!/usr/bin/env python3
"""Classic 3D friction slope-test example using generated_api.

Mirrors ``polyfem-data/contact/examples/3D/friction/high-school-physics-slopetest-mu=0.50.json``.
"""

from __future__ import annotations

import sys
from pathlib import Path

import polyfem
from polyfempy.runtime import solve

EXAMPLE_DIR = Path(__file__).resolve().parent
if str(EXAMPLE_DIR) not in sys.path:
    sys.path.insert(0, str(EXAMPLE_DIR))

from _contact_3d_common import (  # noqa: E402
    CONTACT_EXAMPLES_DIR,
    MESHES_DIR,
)


SOURCE_JSON = (
    CONTACT_EXAMPLES_DIR
    / "3D"
    / "friction"
    / "high-school-physics-slopetest-mu=0.50.json"
)

model = polyfem.model()

rubber = polyfem.neo_hookean(E=1000000000.0, nu=0.4, rho=1000)
steel = polyfem.neo_hookean(E=200000000000.0, nu=0.3, rho=7750)

block = model.mesh(
    mesh=str(MESHES_DIR / "3D" / "simple" / "cube.msh"),
    transformation=polyfem.transformation(
        rotation=[0, 0, -26.565],
        scale=1,
        translation=[0, 0, 0],
    ),
)
block.material(rubber)

slope = model.mesh(
    mesh=str(MESHES_DIR / "3D" / "simple" / "cube.msh"),
    transformation=polyfem.transformation(
        dimensions=[10, 0.01, 10],
        rotation=[0, 0, -26.565],
        translation=[2, -1.566, 0],
    ),
)
slope.material(steel)
slope.surface_all().dirichlet(value=[0, 0, 0])

solver = polyfem.solver(
    linear=polyfem.linear(solver="Eigen::PardisoLDLT"),
    nonlinear=polyfem.nonlinear(
        iterations_per_strategy=1,
        line_search=polyfem.line_search(method="RobustArmijo"),
        solver="Newton",
    ),
    contact=polyfem.solver_contact(
        friction_convergence_tol=0.01,
        friction_iterations=-1,
    ),
    advanced=polyfem.solver_advanced(lump_mass_matrix=True),
)

output = polyfem.output(
    directory="results/3D/friction/high-school-physics-slopetest-mu=0.50",
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
    time_dt=0.025,
    contact=polyfem.contact(
        enabled=True,
        dhat=0.001,
        epsv=1e-05,
        friction_coefficient=0.5,
    ),
    solver=solver,
    output=output,
)


if __name__ == "__main__":
    solve(cfg=polyfem_config)
