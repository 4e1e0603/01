# random walk

_Simulations of various types of random walk._

- Simple random walks
  - [x] Random walk on regular 1D lattice where you can step in any of the two directions `{↑, ↓}` with the same probability.
  - [x] Random walk on regular 2D lattice where you can step in any of the four directions `{↑, ←, ↓, →}` with the same probability.
  - [x] Random walk on regular 3D lattice where you can step in any of the six directions `{↑, ←, ↙, ↓, →, ↗}` with the same probability.

- Restricted random walks
  - [x] Random walk on regular 1/2/3D lattice without immediate return where you can step in three possible directions with the same probability,
      the first step is in any direction.
  - [ ] Random walk on the square lattice without crossing i.e. self-avoiding random walk.

## Examples

### Simple random walks

<p float="left">
<img src="random-walks/output/RandomWalk1D-restricted=False.png" width="30.333%"/>
<img src="random-walks/output/RandomWalk2D-restricted=False.png" width="30.333%"/>
<img src="random-walks/output/RandomWalk3D-restricted=False.png" width="30.333%"/>
</p>

### Restricted random walks

<p float="left">
<img src="random-walks/output/RandomWalk1D-restricted=True.png" width="30.333%"/>
<img src="random-walks/output/RandomWalk2D-restricted=True.png" width="30.333%"/>
<img src="random-walks/output/RandomWalk3D-restricted=True.png" width="30.333%"/>
</p>

### Random walk statistics

<p float="left">
<img src="random-walks/output/RandomWalk2DStatisticsSimple1.png" width="49.5%"/>
<img src="random-walks/output/RandomWalk2DStatisticsSimple2.png" width="49.5%"/>
</p>

<p float="left">
<img src="random-walks/output/RandomWalk2DStatisticsRestricted1.png" width="49.5%"/>
<img src="random-walks/output/RandomWalk2DStatisticsRestricted2.png" width="49.5%"/>
</p>

## Build and run

All outputs such as data and images are located in `output` folder.
The presented images were produced by Python implementation.

See the source files:

- [random_walk.py module](random-walks/source/random_walk.py)
- [random_walk.ipynb notebook](random-walks/source/random_walk.ipynb)
- [random_walk.f90 module](random-walks/source/random_walk.f90)
- [random_walk_main.f90 program](random-walks/source/random_walk_main.f90)
- [random_walk_main.f90 test](random-walks/source/random_walk_test.f90)

### Python

You need Python version 3.10+.

Create a virtual environment.

```powershell
py -3.10 -m venv .venv
.venv\scripts\activate
pip install matplotlib seaborn numpy pandas
```

Note: On Ubuntu may need to install `venv` module as `sudo apt-get install python-venv`. And invoke the 
module as `python3 -m venv .venv` (there is no `py.exe` as on Windows. Please read the official [documentation](https://docs.python.org/3/tutorial/venv.html).

Run the simulations.

```powershell
python .\source\random_walk.py 1_000_000 3 123321 True # 1D simulation with 100_000 steps
                                                   ^------ Run solution (example) (True | False)
                                           ^-------------- Random seed
                                         ^---------------- Dimension (1 | 2 | 3)
                                ^------------------------- Number of steps per walk
```

The running simulation looks like this:

    Run 2D example with statistics: from 1 to 500 steps and 100 repeats per steps.
    trial = 218, walk = 990

&hellip; after succes run:

    ---SUCCESS---

### Fortran

Work-in-progress: The Fortran version is almost finished, but data are not at the shape suitable for analysis.

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
