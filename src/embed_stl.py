""" src/embed_voxels.py

Module to embed voxels representing a geometry as an IBM field array.
"""

import numpy as np

def embed(voxels, mesh_n, mesh_l, shift=[0, 0, 0]):
    """Embeds the voxel data as an IBM within a mesh."""

    nx = mesh_n[0]
    ny = mesh_n[1]
    nz = mesh_n[2]

    dx = mesh_l[0] / (nx - 1)
    dy = mesh_l[1] / (ny - 1)
    dz = mesh_l[2] / (nz - 1)

    n0, nn = _bounds(voxels, mesh_n, [dx, dy, dz], shift)
    print(f"Working range {n0} : {nn}")
    
    ibm = np.ones([nz, ny, nx], dtype=np.double)
    nxyz = np.prod(nn - n0)
    ctr = 0
    workfrac = 0
    for k in range(n0[2], nn[2]):
        for j in range(n0[1], nn[1]):
            for i in range(n0[0], nn[0]):
                x = i * dx - shift[0]
                y = j * dy - shift[1]
                z = k * dz - shift[2]

                # Zero out the embedded body in the mask
                if voxels.query([x, y, z]) > 0:
                    ibm[k,j,i] = 0.0

                if ctr > (workfrac / 100.0) * nxyz:
                    print(f"{workfrac}%")
                    workfrac += 10
                ctr += 1

    return ibm

def _bounds(voxels, nxyz, dxyz, shift):
    """Determines the loop bounds for embedding"""

    x0, xn = voxels.bounding_box()
    x0 = x0 + np.array(shift)
    xn = xn + np.array(shift)

    print(x0)
    print(xn)

    n0 = np.floor(x0 / np.array(dxyz)).astype(int)
    nn = np.floor(xn / np.array(dxyz)).astype(int)

    print(n0)
    print(nn)

    for i in range(3):
        n0[i] = max(n0[i], 0)
        nn[i] = min(nn[i], nxyz[i])

    return [n0, nn]
