""" tests/test_voxels.py
"""

import unittest

import numpy as np
    
from src.voxel import Voxels

class TestVoxels(unittest.TestCase):
    """Tests the basic setup of the Voxels class."""

    def test(self):

        lx = 1.0
        ly = 2.0
        lz = 4.0

        nx = 10
        ny = 5
        nz = 20

        dx = lx / nx
        dy = ly / ny
        dz = lz / nz

        sx = 1 / dx
        sy = 1 / dy
        sz = 1 / dz
        
        # STL-to-Voxels is zyx ordered
        vox = Voxels(np.zeros([nz, ny, nx]),
                     np.array([sx, sy, sz]),
                     np.array([0, 0, 0]))

        self.assertTrue(np.all(vox.n == np.array([nz, ny, nx])))
        self.assertTrue(np.all(vox.L == np.array([lz, ly, lx])))

class TestXYZIJK(unittest.TestCase):
    """Tests converting spatial coordinates to voxel coordinate indices."""

    def setUp(self):
        
        self.lx = 1.0
        self.ly = 2.0
        self.lz = 4.0

        self.nx = 10
        self.ny = 5
        self.nz = 20

        self.dx = self.lx / self.nx
        self.dy = self.ly / self.ny
        self.dz = self.lz / self.nz

        self.sx = 1 / self.dx
        self.sy = 1 / self.dy
        self.sz = 1 / self.dz

        self.ox = 0.75
        self.oy = -3.0
        self.oz = 2.0
        
        # STL-to-Voxels is zyx ordered
        self.vox = Voxels(np.zeros([self.nz, self.ny, self.nx]),
                          np.array([self.sx, self.sy, self.sz]),
                          np.array([self.ox, self.oy, self.oz]))

    def test_inside(self):

        x = self.ox + 0.5 * self.lx
        y = self.oy + 0.5 * self.ly
        z = self.oz + 0.5 * self.lz
        ijk = self.vox._ijk([x, y, z])
        self.assertTrue(np.all(ijk > 0))
        self.assertTrue(np.all(ijk < self.vox.n))

    def test_before(self):

        x = self.ox - 0.1 * self.dx
        y = self.oy - 0.1 * self.dy
        z = self.oz - 0.1 * self.dz
        ijk = self.vox._ijk([x, y, z])
        self.assertTrue(np.all(ijk < 0))

    def test_after(self):

        x = self.ox + self.lx + 0.1 * self.dx
        y = self.oy + self.ly + 0.1 * self.dy
        z = self.oz + self.lz + 0.1 * self.dz
        ijk = self.vox._ijk([x, y, z])
        self.assertTrue(np.all(ijk == self.vox.n))

    def test_past(self):

        x = self.ox + self.lx + 1.1 * self.dx
        y = self.oy + self.ly + 1.1 * self.dy
        z = self.oz + self.lz + 1.1 * self.dz
        ijk = self.vox._ijk([x, y, z])
        self.assertTrue(np.all(ijk > self.vox.n))

    def test_corner0(self):

        x = self.ox
        y = self.oy
        z = self.oz
        ijk = self.vox._ijk([x, y, z])
        self.assertTrue(np.all(ijk == 0))

    def test_cornerN(self):

        x = self.ox + self.lx
        y = self.oy + self.ly
        z = self.oz + self.lz
        ijk = self.vox._ijk([x, y, z])
        self.assertTrue(np.all(ijk == self.vox.n))

class TestQuery(unittest.TestCase):
    """Tests querying the voxel grid at a point in space."""

    def setUp(self):
        
        self.lx = 1.0
        self.ly = 2.0
        self.lz = 4.0

        self.nx = 10
        self.ny = 5
        self.nz = 20

        self.dx = self.lx / self.nx
        self.dy = self.ly / self.ny
        self.dz = self.lz / self.nz

        self.sx = 1 / self.dx
        self.sy = 1 / self.dy
        self.sz = 1 / self.dz

        self.ox = 0.75
        self.oy = -3.0
        self.oz = 2.0
        
        # STL-to-Voxels is zyx ordered
        self.vox = Voxels(np.ones([self.nz, self.ny, self.nx]),
                          np.array([self.sx, self.sy, self.sz]),
                          np.array([self.ox, self.oy, self.oz]))

    def test_inside(self):

        x = self.ox + 0.5 * self.lx
        y = self.oy + 0.5 * self.ly
        z = self.oz + 0.5 * self.lz
        q = self.vox.query([x, y, z])
        self.assertTrue(q == 1)

    def test_before(self):

        x = self.ox - 0.1 * self.dx
        y = self.oy - 0.1 * self.dy
        z = self.oz - 0.1 * self.dz
        q = self.vox.query([x, y, z])
        self.assertTrue(q == 0)
        
    def test_after(self):

        x = self.ox + self.lx + 0.1 * self.dx
        y = self.oy + self.ly + 0.1 * self.dy
        z = self.oz + self.lz + 0.1 * self.dz
        q = self.vox.query([x, y, z])
        self.assertTrue(q == 0)

    def test_corner0(self):

        x = self.ox
        y = self.oy
        z = self.oz
        q = self.vox.query([x, y, z])
        self.assertTrue(q == 1)

    def test_cornerN(self):

        x = self.ox + self.lx
        y = self.oy + self.ly
        z = self.oz + self.lz
        q = self.vox.query([x, y, z])
        self.assertTrue(q == 1)
