# py4x3d2

Tooling for the new x3d2 solver.

`py4x3d2` supports generating IBM masks for `x3d2`.
There are currently two mask generators:
1) `run.py` will load an `stl` file (currently hardcoded) and embed this into a mesh
2) `tests/run.py` generates a cylinder mask

## Dependencies

`py4x3d2` depends on `ADIOS2` to write the IBM mask for loading into `x3d2`.

To read `stl` files `py4x3d2` depends on `stl-to-voxel`, installable via `pip`.
