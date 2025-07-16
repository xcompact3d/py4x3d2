import numpy as np
import adios2
if hasattr(adios2, "__version__"):
    adios2_minor = int(adios2.__version__.split('.')[1])
    if adios2_minor >= 10:
        from adios2 import Stream
        adios2_new_api = True
    else:
        adios2_new_api = False
else:
    # Assume old API
    adios2_new_api = False

import src.convert_stl as convert_stl
import src.embed_stl as embed_stl

def run(stl_file):

    # Convert STL to voxel array
    voxels = convert_stl.convert(stl_file)

    print(f"Object dimensions: {voxels.dims()}")
    print(f"Voxel scale: {voxels.scale}")
    print(f"Voxel size: {1 / voxels.scale}")
    print(f"Voxel count: {voxels.count()}")
    print(f"Bounding box: {voxels.bounding_box()}")
    
    # Embed voxels into an IBM field
    # mesh_n = [350, 950, 215]
    mesh_n = [697, 1878, 429]
    # mesh_l = [39.6, 92.4, 236]
    # mesh_l = [72, 160, 32]
    # mesh_l = [60, 162, 37]
    mesh_l = [60.11421911, 161.97202797,  37. ]
    shift = [0, 0, 0]
    ibm = embed_stl.embed(voxels, mesh_n, mesh_l, shift)

    shift = [-13.244, 29.2215, 0]
    ibm2 = embed_stl.embed(voxels, mesh_n, mesh_l, shift)

    ibm = ibm2 * ibm
    
    # Write voxel array using ADIOS2
    nx = ibm.shape[0]
    ny = ibm.shape[1]
    nz = ibm.shape[2]

    shape = [nx, ny, nz]
    start = [0, 0, 0]
    count = [nx, ny, nz]

    if not adios2_new_api:
        with adios2.open("test.bp4", "w") as fh:
            fh.write("iibm", np.array([1]))
            fh.write("ep1", np.ascontiguousarray(ibm), shape, start, count)
    else:
        with Stream("ibm.bp4", "w") as s:
            # Basic IBM
            s.write("iibm", 1)
            s.write("ep1", np.ascontiguousarray(ibm), shape, start, count, operations=None)


if __name__ == "__main__":
    #run("/Users/paulbartholomew/DATA/mesh/stl/test_single_foil.stl")
    run("front_foil.stl")
