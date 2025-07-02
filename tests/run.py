#!/usr/bin/env python3
import numpy as np
from adios2 import Stream
from test_cylinder import *
import argparse

#
# Default values
#
default_iibm = 1
default_nx = 32
default_ny = default_nx
default_nz = default_nx
default_dx = 0.1
default_dy = default_dx
default_dz = default_dx
default_save = True
default_verbose = True
output = "ibm"

#
# Process arguments
#
parser = argparse.ArgumentParser(description='Generate IBM input for x3d2')
parser.add_argument('-v', '--verbose', type=bool, default=default_verbose, action=argparse.BooleanOptionalAction)
parser.add_argument('-i', '--iibm', type=int, default=default_iibm, help='type of IBM')
parser.add_argument('--dx', type=float, default=default_dx, help='step of the mesh in x')
parser.add_argument('--dy', type=float, default=default_dy, help='step of the mesh in y')
parser.add_argument('--dz', type=float, default=default_dz, help='step of the mesh in z')
parser.add_argument('--nx', type=int, default=default_nx, help='number of cells in x')
parser.add_argument('--ny', type=int, default=default_ny, help='number of cells in y')
parser.add_argument('--nz', type=int, default=default_nz, help='number of cells in z')
parser.add_argument('--save', type=bool, default=default_save, help='save profiles', action=argparse.BooleanOptionalAction)
parser.add_argument('--cyl', nargs=7, 
                             metavar=('Rcyl', 'x0', 'y0', 'z0', 'ax', 'ay', 'az'),
                             help="Define a cylinder with radius Rcyl, position (x0, y0, z0) and axis (ax, ay, az)", 
                             type=float,
                             default=None)
args = parser.parse_args()

#
# Print some stuff
#
if args.verbose:
    print("IBM preprocessor")
    print("  Type of IBM : " + str(args.iibm))
    print("  Step of the mesh : " + str(args.dx) + " " + str(args.dy) + " " + str(args.dz))
    print("  Number of cells : " + str(args.nx) + " " + str(args.ny) + " " + str(args.nz))
    print("  Generate the IBM input : " + str(args.save))
    print("  Cylinder : " + str(args.cyl))

#
# Parameters
#
iibm = args.iibm
nx = args.nx
ny = args.ny
nz = args.nz
dx = args.dx
dy = args.dy
dz = args.dz

#
# Generate the mask
#
mask = np.ones((nz, ny, nx), dtype=np.double)
if args.cyl:
    mask = mask * gencyl([dz, dy, dx], 
                         [nz, ny, nx], 
                         args.cyl[0], 
                         [args.cyl[3], args.cyl[2], args.cyl[1]], 
                         [args.cyl[6], args.cyl[5], args.cyl[4]])

#
# Ouptut to ADIOS2
#
if args.save:
    with Stream("ibm.bp", "w") as s:
        # Basic IBM
        s.write("iibm", 1)
        s.write("ep1", np.ascontiguousarray(mask), shape=[nx, ny, nz], start=[0,0,0], count=[nx, ny, nz], operations=None)
