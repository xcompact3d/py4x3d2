""" src/embed_stl.py

Module to embed voxels representing a geometry as an IBM field array.
"""

import numpy as np

def embed(voxels, mesh_n, mesh_l, shift=[0, 0, 0]):
    """Embeds the voxel data as an IBM within a mesh."""

    nx, ny, nz = mesh_n
    dx = mesh_l[0] / (nx - 1) if nx > 1 else 0
    dy = mesh_l[1] / (ny - 1) if ny > 1 else 0
    dz = mesh_l[2] / (nz - 1) if nz > 1 else 0

    # calculate center of the voxel object from its bounding box
    bbox_min, bbox_max = voxels.bounding_box()
    voxel_center = (bbox_min + bbox_max) / 2.0

    # calculate the offset vector needed to move the voxel's center
    # to the desired final 'shift' location in the domain.
    offset = np.array(shift) - voxel_center

    # determine the loop bounds in the final grid using the correct offset
    n0, nn = _bounds(voxels, mesh_n, [dx, dy, dz], offset)
    print(f"Working range (indices): {n0} -> {nn}")

    ibm = np.ones([nz, ny, nx], dtype=np.float64)
    for k in range(n0[2], nn[2]):
        for j in range(n0[1], nn[1]):
            for i in range(n0[0], nn[0]):
                x_global = np.array([i * dx, j * dy, k * dz])

                x_local = x_global - offset

                if voxels.query(x_local) > 0:
                    ibm[k, j, i] = 0.0

    return ibm

def _bounds(voxels, nxyz, dxyz, offset):
    """Determines the loop bounds for embedding using the correct offset."""

    x0, xn = voxels.bounding_box()

    x0_global = x0 + offset
    xn_global = xn + offset

    # convert the final physical coordinates to grid indices
    # handle dxyz=0 for 2D cases to avoid division by zero
    dxyz_safe = np.array([d if d > 0 else 1 for d in dxyz])
    n0 = np.floor(x0_global / dxyz_safe).astype(int)

    nn = np.ceil(xn_global / dxyz_safe).astype(int)

    nx, ny, nz = nxyz
    n0[0] = max(n0[0], 0)
    n0[1] = max(n0[1], 0)
    n0[2] = max(n0[2], 0)
    nn[0] = min(nn[0], nx)
    nn[1] = min(nn[1], ny)
    nn[2] = min(nn[2], nz)

    return [n0, nn]
