# Random walks

_Simplictic simulations of various types of random walks._

- Simple random walks
  - [x] Random walk on regular 1D lattice where you can step in any of the two directions `{↑, ↓}` with the same probability.
  - [x] Random walk on regular 2D lattice where you can step in any of the four directions `{↑, ←, ↓, →}` with the same probability.
  - [x] Random walk on regular 3D lattice where you can step in any of the six directions `{↑, ←, ↙, ↓, →, ↗}` with the same probability.

- Restricted random walks
  - [ ] Random walk on regular lattice without immediate return where you can step in three possible directions with the same probability,
      the first step is in any direction.
  - [ ] Random walk on the square lattice without crossing i.e. self-avoiding random walk.

See the examples:

- [random_walk.py module](source/random_walk.py)⌈
- [random_walk.f90 module](source/random_walk.f90)
- [random_walk_main.f90 program](source/random_walk.f90)

![Random walk 1D](output/RandomWalk1D.png "Random walk 1D")
![Random walk 2D](output/RandomWalk2D.png "Random walk 2D")
![Random walk 2D](output/RandomWalk3D.png "Random walk 3D")

## Build and run

### Fortran

Work-in-progress

Compile and run *main* program:

```powershell
gfortran source\random_walk.f90 source\random_walk_main.f90 -o build\random_walk_main.exe
.\random_walk_main.exe 123 100 1 > data.psv
```

Compile and run *test* program:

```powershell
gfortran source\random_walk.f90 source\random_walk_test.f90 -o build\random_walk_test.exe
.\build\random_walk_test.exe
```

Also, you can execute the `project.bat` with `build` command and then run programs:

```powershell
.\project.bat build

.\build\random_walk_main.exe 123 100 1
.\build\random_walk_test.exe
```

### Python

You need Python version 3.10+.

Create virtual environment.

      py -3.10 -m venv .venv
      .venv\scripts\activate
      pip install matplotlib, seaborn, numpy, pandas

Run the simulations.

      py source\random_walk.py 100_000 1    # 1D simulation with 100_000 steps
      py source\random_walk.py 100_000 2    # 2D simulation with 100_000 steps
