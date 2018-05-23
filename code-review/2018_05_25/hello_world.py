#!/usr/bin/env python 

from __future__ import print_function

from mpi4py import MPI

comm = MPI.COMM_WORLD # Communicator for the processes.
rank = comm.Get_rank() # What number process is this one?
size = comm.Get_size() # How many processes in total are there?

print("I am Rank {0} of {1}: Hello World!".format(rank, size))
