""" src/voxel.py

Class definition of voxels.
"""

import numpy as np

class Voxels:
    def __init__(self, vol, scale, shift):
        """Stores a voxel object based on the representation from stl-to-voxel.

        Note that stl-to-voxel stores voxel data in [zyx] order, but the scale and shift arrays are
        [xyz]. To prevent costly transposes the data is stored in this same order, users should use
        the interface methods to simplify access to the voxel object.
        """

        self.vol = vol
        self.scale = scale
        self.shift = shift

        # Store the voxel array shape and object dimensions in [zyx] ordering to simplify working
        # with the voxel data layout.
        self.n = vol.shape
        self.L = self.n / np.flip(self.scale)
        
    def _xyz(self, xyz):
        """Get the relative spatial coordinate.

        Note that shift is stored as [sx, sy, sz], therefore you should pass [x,y,z] despite the
        voxels being stored in [z,y,x] order.
        """
        
        return xyz - self.shift

    def _ijk(self, xyz):
        """Converts a spatial [x,y,z] coordinate into voxel indices [z,y,x]."""

        xyz_rel = self._xyz(xyz)

        # XXX: np.floor(x) rounds DOWN, not towards zero - this is the behaviour that we want as it
        #      prevents points that are -ve in relative space from being rounded into the object.
        # XXX: The relative coordinates are flipped as stl voxels are stored in [zyx] order.
        ijk = np.flip(np.floor(xyz_rel * self.scale).astype(int))

        return ijk
        
    def query(self, xyz):
        """Obtains the voxel value at coordinates [xyz]."""

        def fix_boundary_intersection(xyz, ijk):
            xyz_rel = np.flip(self._xyz(xyz)) # Flip coordinates as stl-to-voxel stores [z,y,x] data
            if np.any(xyz_rel == self.L):
                for i in range(3):
                    if (xyz_rel[i] == self.L[i]):
                        ijk[i] -= 1
                return self.vol[ijk[0], ijk[1], ijk[2]]
            else:
                return 0

        ijk = self._ijk(xyz)
        if np.any(ijk < 0) or np.any(ijk > self.n):
            return 0
        elif np.any(ijk == self.n):
            return fix_boundary_intersection(xyz, ijk)
        else:
            return self.vol[ijk[0], ijk[1], ijk[2]]

    def dims(self):
        """Returns the dimensions of the object."""

        return np.flip(self.L)

    def bounding_box(self):
        """Returns the limits of the bounding box as a coordinate pair."""

        x0 = self.shift
        xn = x0 + self.dims()
        return [x0, xn]

    def count(self):
        """Returns the number of voxels representing the object."""

        return np.flip(self.n)
        
