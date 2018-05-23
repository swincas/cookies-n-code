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

# Then pass all the values to rank 0 to find the global mean.
if rank == 0:
    mean_array = np.empty(size)
    mean_array[0] = local_mean

    for i in range(1,size):
        mean_array[i] = comm.recv(source=i, tag=11)

    print("I am rank {0} and the mean from 0 to {1} is {2}".format(rank,
          N, np.mean(mean_array))) 

else:
    comm.send(local_mean, dest=0, tag=11)


