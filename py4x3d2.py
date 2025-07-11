from mpi4py import MPI
import numpy as np
import adios2

import src.convert_stl as convert_stl

def run(stl_file):

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
        
    vol = convert_stl.convert(stl_file)

    nx = vol.shape[0]
    ny = vol.shape[1]
    nz = vol.shape[2]

    shape = [nx, ny, nz]
    start = [0, 0, 0]
    count = [nx, ny, nz]

    with adios2.open("test.bp", "w", comm) as fh:
        for _ in range(0, 1):
            fh.write("vol", vol, shape, start, count)
