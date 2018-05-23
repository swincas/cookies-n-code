#!/usr/bin/env python

from __future__ import print_function

import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD # Communicator for the processes.
rank = comm.Get_rank() # What number process is this one?
size = comm.Get_size() # How many processes in total are there?

if rank == 0: # Only rank 0 will have the data.
    data = np.arange(10)
    comm.send(data, dest=1, tag=11)
else: # All the other ranks will receive their data from rank 0.
    data = comm.recv(source=0, tag=11)

print("I am rank {0} and my data is {1}".format(rank, data))




