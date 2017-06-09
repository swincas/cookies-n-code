#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import print_function
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
name = MPI.Get_processor_name()

print("Hello, World! I am MPI task {0} of {1} on {2}".format(rank, size, name))

