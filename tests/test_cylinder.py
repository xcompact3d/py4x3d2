"""
Unit test for the cylinder module.
"""

import unittest

import numpy as np

NX=10
NY=10
NZ=10
LX=1.0
LY=1.0
LZ=1.0
DX=LX/(NX-1)
DY=LY/(NY-1)
DZ=LZ/(NZ-1)

RCYL=0.5

#
# Compute the radius
#
# Inputs : 3D vector (i,j,k) and (dx, dy, dz)
# Output : radius for each (i,j,k) point
#
def get_radius(ijk, dxyz):
    #
    # Cartesian coordinates
    #
    x = ijk[0] * dxyz[0]
    y = ijk[1] * dxyz[1]
    z = ijk[2] * dxyz[2]
    #
    # Return the associated radius
    # FIXME origin and axis of the cylinder can change
    #
    return (x**2 + y**2)**0.5

#
# Generate the mask associated with the cylinder
#
# Inputs : 3D vector (dx, dy, dz), number of points (nx, ny, nz)
# Output : mask in a 3D array, Fortran order
#
def gencyl(dxyz, n, rcyl):
    #
    # Allocate and init to zero
    #
    mask = np.zeros(n, order='F')
    #
    # One when the radius is below rcyl
    #
    for idx, _ in np.ndenumerate(mask):
        if get_radius(idx, dxyz) <= rcyl:
            mask[idx] = 1.0
    #
    # Done
    #
    return mask

                
class TestMask(unittest.TestCase):
    """Test that the mask has been computed correctly: 1 for interior points, 0 for exterior
    points."""
    
    def test_x(self):

        mask = gencyl([DX, DY, DZ], [NX, NY, NZ], RCYL)
        
        for i in range(NX):
            for j in range(NY):
                for k in range(NZ):

                    r = get_radius([i, j, k], [DX, DY, DZ])
                    if r > RCYL:
                        self.assertEqual(mask[i][j][k], 0.0)
                    elif r < RCYL:
                        self.assertEqual(mask[i][j][k], 1.0)

# class TestDistance(unittest.TestCase):
#     """Test that the distance from the surface is correct: exterior points are at a positive
#     distance, interior points are at a negative distance."""
#     pass

# class TestDirection(unittest.TestCase):
#     """Test that the direction vector is correct: it should point to the nearest surface point."""
#     pass

if __name__ == '__main__':
    unittest.main()
