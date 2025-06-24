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

def get_radius(ijk, dxyz):
    """Computes the radius of a grid coordinate relative to the origin.

    :param ijk:  The grid coordinates (i,j,k)
    :param dxyz: The grid spacing (dx,dy,dz)
    :return:     Radius of the point from the origin.
    """
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

def gencyl(dxyz, n, rcyl):
    """Generates a mask array representing a cylinder.

    :param dxyz: The grid spacing (dx,dy,dz)
    :param n:    The grid dimensions (nx,ny,nz)
    :param rcyl: The cylinder radius
    :return:     Mask array of 0s for exterior points, 1s for interior points.
    """
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
