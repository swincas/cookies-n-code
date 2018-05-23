#!/usr/bin/env python

from __future__ import print_function

import numpy as np
import math
from mpi4py import MPI

comm = MPI.COMM_WORLD # Communicator for the processes.
rank = comm.Get_rank() # What number process is this one?
size = comm.Get_size() # How many processes in total are there?

N = 1e9

if N % size != 0:
    print("Choose a number of processors that equally divides the number of "
          "elements in the array.  Current number of elements is "
          "{0}".format(N))
    raise ValueError

# First determine the range of numbers this process will handle.
lower_range = int(N/size * rank)
upper_range = int(N/size * (rank+1))
data = np.arange(lower_range, upper_range)
local_mean = np.mean(data)

print("I am rank {0} and my local mean is {1}".format(rank, local_mean))

global_sum = comm.reduce(local_mean, op=MPI.SUM)

if rank == 0:
    print("I am rank {0} and the mean from 0 to {1} is {2}".format(rank,
          N, global_sum / size))




