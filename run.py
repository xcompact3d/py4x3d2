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

    print(f"Model dimensions: {voxels.L}")
    print(f"Model scale: {voxels.scale}")
    print(f"Voxel size: {1 / voxels.scale}")
    print(f"Voxel count: {voxels.n}")
    print(f"Bounding box: {voxels.bounding_box()}")

    # Embed voxels into an IBM field
    # mesh_n = [350, 950, 215]
    # mesh_n = [608, 1632, 384]
    mesh_n = [697, 1878, 429] # nx, ny, nz
    ratio = 1
    mesh_n = [697/ratio, 1878/ratio, 429/ratio]
    mesh_n = [ int(a) for a in mesh_n ]
    # mesh_l = [39.6, 92.4, 236]
    # mesh_l = [72, 160, 32]
    # mesh_l = [60, 162, 37]
    mesh_l = [60.11421911, 161.97202797, 37.0]  # Lx, Ly, Lz

    # get the geometric centre of the original stl object
    bbox_min, bbox_max = voxels.bounding_box()
    stl_centre = (bbox_min + bbox_max) / 2.0

    # define the desired centre for the entire two-foil system
    system_centre = np.array([
        mesh_l[0] / 2.0,
        mesh_l[1] / 2.0,
        mesh_l[2] / 2.0
    ])

    # use relative shift
    relative_offset = np.array([-13.244, 29.2215, 0.0])

    # calculate the final absolute positions for each foil's centre
    centre_pos_1 = system_centre - relative_offset / 2.0
    centre_pos_2 = system_centre + relative_offset / 2.0

    # embed first foil at its final calculated position
    ibm1 = embed_stl.embed(voxels, mesh_n, mesh_l, centre_pos_1)

    # embed second foil at its final calculated position
    ibm2 = embed_stl.embed(voxels, mesh_n, mesh_l, centre_pos_2)

    # combine the masks
    ibm = ibm1 * ibm2

    # shape of the numpy array is (nz, ny, nx)
    nz, ny, nx = ibm.shape
    
    shape = [nz, ny, nx]
    start = [0, 0, 0]
    count = [nz, ny, nx]

    if not adios2_new_api:
        with adios2.open("test.bp4", "w") as fh:
            fh.write("iibm", np.array([1]))
            fh.write("ep1", np.ascontiguousarray(ibm), shape, start, count)
    else:
        with Stream("ibm.bp", "w") as s:
            # Basic IBM
            s.write("iibm", 1)
            s.write("ep1", np.ascontiguousarray(ibm), shape, start, count, operations=None)

    print("\nSuccessfully generated clean ibm.bp file.")

if __name__ == "__main__":
    run("front_foil.stl")
