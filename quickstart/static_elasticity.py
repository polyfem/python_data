"""Solve a small elastic square under a uniform body load."""

from pathlib import Path
from tempfile import TemporaryDirectory

import polyfem
from polyfempy import Result, solve


def main() -> Result:
    with TemporaryDirectory() as folder:
        mesh = Path(folder) / "square.obj"
        mesh.write_text(
            "v 0 0 0\nv 1 0 0\nv 1 1 0\nv 0 1 0\nv .5 .5 0\n"
            "f 1 2 5\nf 2 3 5\nf 3 4 5\nf 4 1 5\n",
            encoding="utf-8",
        )

        model = polyfem.model()
        square = model.mesh(mesh=str(mesh))
        square.material(polyfem.linear_elasticity(E=1000, nu=0.3))
        square.dirichlet(value=[0, 0])
        square.rhs(value=[0, -1])
        model.solver(linear=polyfem.linear(solver="Eigen::SimplicialLDLT"))

        result = solve(cfg=model.config())
        print(f"Largest displacement component: {abs(result.sol).max():.8g}")
        return result


if __name__ == "__main__":
    main()
