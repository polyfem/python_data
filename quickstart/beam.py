"""Solve a cantilever beam with a downward body force, using SI units."""

from pathlib import Path

import polyfem
from polyfempy import Result, solve


def main() -> Result:
    model = polyfem.model()
    mesh = Path(__file__).with_name("beam.obj")
    beam = model.mesh(mesh=str(mesh))
    beam.material(polyfem.linear_elasticity(E=1e7, nu=0.3))

    # Fix the left end at x = 0.
    left = beam.surface_axis(axis="-x", position=0.0)
    left.dirichlet(value=[0, 0])

    # Apply a downward body force (N/m^3).
    beam.rhs(value=[0, -1000])
    model.solver(linear=polyfem.linear(solver="Eigen::SimplicialLDLT"))

    result = solve(cfg=model.config())
    print(f"Largest displacement component: {abs(result.sol).max():.6f} m")
    return result


if __name__ == "__main__":
    main()
