""" src/convert_stl.py

Module to load and convert an STL file to a Numpy array that we can write.
"""

import stl
import stltovoxel as stv
import numpy as np

from . import voxel

def convert(stl_file):
    """ Converts an stl file into a Numpy array.
    """
    #
    # This function is based on the implementation of `convert_files()` in the `stl-to-voxel`
    # package, released under the following MIT license:
    #
    #   The MIT License (MIT)
    #
    #   Copyright (c) 2015 Christian Pederkoff
    #
    #   Permission is hereby granted, free of charge, to any person obtaining a copy of this
    #   software and associated documentation files (the "Software"), to deal in the Software
    #   without restriction, including without limitation the rights to use, copy, modify, merge,
    #   publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
    #   to whom the Software is furnished to do so, subject to the following conditions:
    #
    #   The above copyright notice and this permission notice shall be included in all copies or
    #   substantial portions of the Software.
    #
    #   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
    #   INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
    #   PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
    #   FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
    #   OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    #   DEALINGS IN THE SOFTWARE.
    #
    
    mesh_obj = stl.mesh.Mesh.from_file(stl_file)
    org_mesh = np.hstack(
        (
            mesh_obj.v0[:, np.newaxis],
            mesh_obj.v1[:, np.newaxis],
            mesh_obj.v2[:, np.newaxis]
        )
    )

    # Returns:
    # - vol:   The voxel grid
    # - scale: The number of voxels per unit length
    # - shift: The distance from the origin to the mesh centre
    # TODO: Currently the voxel resolution is hardcoded, in future this could be determined in
    #       combination with the x3d2 mesh resolution.
    resolution = 400
    vol, scale, shift = stv.convert_meshes([org_mesh], resolution, None, False)

    return voxel.Voxels(vol, scale, shift)
