#!/usr/bin/env python 

from __future__ import print_function

import os
import random
import numpy as np
import time

from mpi4py import MPI

comm = MPI.COMM_WORLD # Communicator for the processes.
rank = comm.Get_rank() # What number process is this one?
size = comm.Get_size() # How many processes in total are there?

def check_Nproc(N):

    if N % size != 0:
        print("Choose a number of processes that equally divides the number of "
              "elements in the array.  Current number of elements is "
              "{0} and number of processes is {1}".format(N, size))
        comm.Abort() 


def hello_world():

    print("I am Rank {0} of {1}: Hello World!".format(rank, size))


def send_recv():

    if size == 1:
        print("This function sends data to other ranks.  It can't on with one "
              "process!")
        raise RuntimeError

    if rank == 0: # Only rank 0 will have the data.
        data = np.arange(10)
        comm.send(data, dest=1, tag=11)
    else: # All the other ranks will receive their data from rank 0.
        data = comm.recv(source=0, tag=11)

    print("I am rank {0} and my data is {1}".format(rank, data))


def send_recv_mean(N=1e6):

    check_Nproc(N)

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


def reduce_example(N=1e6):

    check_Nproc(N)

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


def reduce_array_example(N=100, num_bins=10):

    data = np.array(random.sample(range(0, N), num_bins)) 

    print("I am rank {0} and my data is {1}".format(rank, data))

    mean_data = np.zeros_like(data)

    comm.Reduce([data, MPI.DOUBLE], [mean_data, MPI.DOUBLE], op=MPI.SUM, root = 0)

    if rank == 0:
        print("I am rank {0} and the mean is {1}".format(rank, mean_data / size))


def my_example(datadir="./data", firstfile=0, lastfile=11):

    # If there aren't any data files, create some data.
    fname = "{0}/data_{1}".format(datadir, firstfile)
    if rank == 0 and not os.path.isfile(fname):
        print("Creating data files to read from.")
        create_data(datadir=datadir, firstfile=firstfile, lastfile=lastfile)
        print("Done!")
    
    comm.Barrier()  # Rank 0 may still be creating data so wait here.

    sum_thistask = 0  # Initialize.
    N_thistask = 0

    # Now each Task will get its own set of files to read in.  
    # This loop ensures each file is only read one.
    for filenr in range(firstfile + rank, lastfile + 1, size):

        fname = "{0}/data_{1}".format(datadir, filenr)
        data_thisfile = np.loadtxt(fname)

        # Sum up the data from this file.
        sum_thistask += sum(data_thisfile)
        N_thistask += len(data_thisfile)

    # Then after all files have been read, reduce everything onto rank 0.
    global_sum = comm.reduce(sum_thistask, op=MPI.SUM)
    global_N = comm.reduce(N_thistask, op=MPI.SUM)
   
    print("I am rank {0} and I processed a total of {1} values.".format(rank,
          N_thistask))

    if rank == 0:
        print("I am rank {0} and {1} total values were processed with a sum "
              "of {2} and a mean of {3}".format(rank, global_N, global_sum,
                                                global_sum / global_N))


def create_data(datadir="./data", firstfile=0, lastfile=11, N_lower=5e5,
                N_upper=6e5):

    for filenr in range(firstfile + rank, lastfile + 1, size):
        N = random.randint(N_lower, N_upper + 1)
        data = np.array(random.sample(range(-int(N_lower*3), int(N_upper*3)), N))

        fname = "{0}/data_{1}".format(datadir, filenr)
        np.savetxt(fname, data) 

if __name__ == "__main__":

    #hello_world()
    #send_recv()
    #send_recv_mean()
    #reduce_example()
    #reduce_array_example()
    my_example()
