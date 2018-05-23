#!/usr/bin/env python

from __future__ import print_function

import numpy as np
import math
import random
from mpi4py import MPI

comm = MPI.COMM_WORLD # Communicator for the processes.
rank = comm.Get_rank() # What number process is this one?
size = comm.Get_size() # How many processes in total are there?

N = 100
num_points = 10

data = np.array(random.sample(range(0, N), num_points)) 

print("I am rank {0} and my data is {1}".format(rank, data))

mean_data = np.zeros_like(data)

comm.Reduce([data, MPI.DOUBLE], [mean_data, MPI.DOUBLE], op=MPI.SUM, root = 0)

if rank == 0:
    print("I am rank {0} and the mean is {1}".format(rank, mean_data / size))


