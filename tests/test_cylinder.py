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

def get_point_radius(x, origin, axis):
    """Computes the radius of a point relative to a line given by origin and axis.

    :param x:      The point in space
    :param origin: The origin vector for the cylinder axis
    :param axis:   The vector along the cylinder axis
    :return:       Radius of the point from the origin.
    """

    # The distance between a point x and a line given by axis a and origin o is given by
    #    |(x - o) X a| / |a|

    c = np.cross(x - origin, axis)
    delta = np.linalg.norm(c) / np.linalg.norm(axis)
    
    return delta
    
def get_grid_point(ijk, dxyz):
    """Computes the spatial coordinate given a grid reference.

    :param ijk:  The grid coordinates (i,j,k)
    :param dxyz: The grid spacing (dx,dy,dz)
    :return:     The spatial coordinate of the grid reference
    """

    return np.array([ijk[i] * dxyz[i] for i in range(3)])

def get_grid_radius(ijk, dxyz, origin, axis):
    """Computes the radius of a grid coordinate relative to a line given by origin and axis.

    :param ijk:    The grid coordinates (i,j,k)
    :param dxyz:   The grid spacing (dx,dy,dz)
    :param origin: The origin vector for the cylinder axis
    :param axis:   The vector along the cylinder axis
    :return:       Radius of the point from the origin.
    """
    
    x = get_grid_point(ijk, dxyz)
    return get_point_radius(x, origin, axis)

def gencyl(dxyz, n, rcyl, origin, axis):
    """Generates a mask array representing a cylinder.

    :param dxyz:   The grid spacing (dx,dy,dz)
    :param n:      The grid dimensions (nx,ny,nz)
    :param rcyl:   The cylinder radius
    :param origin: The origin vector for the cylinder axis
    :param axis:   The vector along the cylinder axis
    :return:       Mask array of 0s for exterior points, 1s for interior points.
    """
    #
    # Allocate and init to zero
    #
    mask = np.ones(n, order='F')
    #
    # One when the radius is below rcyl
    #
    for idx, _ in np.ndenumerate(mask):
        if get_grid_radius(idx, dxyz, origin, axis) <= rcyl:
            mask[idx] = 0.0
    
    return mask

                
class TestMask(unittest.TestCase):
    """Test that the mask has been computed correctly: 1 for interior points, 0 for exterior
    points."""
    
    def test_x(self):

        mask = gencyl([DX, DY, DZ], [NX, NY, NZ], RCYL, [0, 0, 0], [0, 0, 1])
        
        for i in range(NX):
            for j in range(NY):
                for k in range(NZ):

                    r = get_grid_radius([i, j, k], [DX, DY, DZ], [0, 0, 0], [0, 0, 1])
                    if r > RCYL:
                        self.assertEqual(mask[i][j][k], 1.0)
                    elif r < RCYL:
                        self.assertEqual(mask[i][j][k], 0.0)

# class TestDistance(unittest.TestCase):
#     """Test that the distance from the surface is correct: exterior points are at a positive
#     distance, interior points are at a negative distance."""
#     pass

# class TestDirection(unittest.TestCase):
#     """Test that the direction vector is correct: it should point to the nearest surface point."""
#     pass

if __name__ == '__main__':
    unittest.main()
