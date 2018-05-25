#!/usr/bin/env python

from __future__ import print_function

import os
import random
import numpy as np

from mpi4py import MPI

comm = MPI.COMM_WORLD  # Communicator for the processes.
rank = comm.Get_rank()  # What number process is this one?
size = comm.Get_size()  # How many processes in total are there?


def check_Nproc(N):
    """
    Ensures that an array with `N` elements can be equally divided among the
    processes.

    If not, abort the program.

    Parameters
    ----------

    N: Integer. Required.
        Number of elements in array.

    Returns
    ----------

    None.

    comm.Abort() is called if the elements cannot be equally divided among
    processes.
    """

    if N % size != 0:
        print("Choose a number of processes that equally divides the number "
              "of elements in the array.  Current number of elements is {0} "
              "and number of processes is {1}".format(N, size))
        comm.Abort()


def hello_world():
    """
    Prints Hello World on each rank.

    Parameters
    ----------

    None.

    Returns
    ----------

    None.
    """

    print("I am Rank {0} of {1}: Hello World!".format(rank, size))


def send_recv():
    """
    Manually sends data from rank 0 process to other processes.

    If program is executed with only 1 process, raises a RuntimeError.

    Parameters
    ----------

    None.

    Returns
    ----------

    None.
    """

    if size == 1:
        print("This function sends data to other ranks.  It can't on with one "
              "process!")
        raise RuntimeError

    if rank == 0:  # Only rank 0 will have the data.
        data = np.arange(10)
        comm.send(data, dest=1, tag=11)
    else:  # All the other ranks will receive their data from rank 0.
        data = comm.recv(source=0, tag=11)

    print("I am rank {0} and my data is {1}".format(rank, data))


def send_recv_mean(N=1e6):
    """
    Each process takes an equal slice of numbers from 0 to N and calculates the
    local mean.  These are then passed back to rank 0 to determine the global
    mean.

    If N numbers does not divide equally among the specified number of
    processes, a RuntimeError is raised.

    Parameters
    ----------

    N: Integer. Default: 1e6.
        Calculate the mean of integers from 0 to N.

    Returns
    ----------

    None.
    """

    check_Nproc(N)  # Ensure that the array can be spread across processes.

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

        for i in range(1, size):
            mean_array[i] = comm.recv(source=i, tag=11)

        print("I am rank {0} and the mean from 0 to {1} is {2}".format(rank,
              N, np.mean(mean_array)))

    else:
        comm.send(local_mean, dest=0, tag=11)


def reduce_example(N=1e6):
    """
    Each process takes an equal slice of numbers from 0 to N and the global
    mean is reduced onto rank 0.

    If N numbers does not divide equally among the specified number of
    processes, a RuntimeError is raised.

    Parameters
    ----------

    N: Integer. Default: 1e6.
        Calculate the mean of integers from 0 to N.

    Returns
    ----------

    None.
    """

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
    """
    Calculates the mean of numbers across bins.  Used to showcase that mpi4py
    can communicate arrays across processes.

    Parameters
    ----------

    N: Integer. Default: 100.
        Largest data point to be summed.

    num_bins: Integer. Default: 10.
        Number of bins that we are summing within.

    Returns
    ----------

    None.
    """

    data = np.array(random.sample(range(0, N), num_bins))

    print("I am rank {0} and my data is {1}".format(rank, data))

    mean_data = np.zeros_like(data)

    comm.Reduce([data, MPI.DOUBLE], [mean_data, MPI.DOUBLE], op=MPI.SUM,
                root=0)

    if rank == 0:
        print("I am rank {0} and the mean is {1}"
              .format(rank, mean_data / size))


def my_example(datadir="./data", firstfile=0, lastfile=11):
    """
    Calculates the mean for numbers across different data files.  Used to
    showcase the strength of mpi4py being able to open different files and
    communicating the results back to root.

    If the data files do not exist, creates files containing random numbers.

    Parameters
    ----------

    datadir: String. Default: './data'.
        The directory the data files are located in.

    firstfile, lastfile: Integers.  Default: 0, 11.
        The range of file numbers that are being read.

    Returns
    ----------

    None.
    """

    print("Running my example in parallel.")

    # Check to see if the data directory exists.
    if not os.path.exists(datadir) and rank == 0:
        os.makedirs(datadir)

    # If there aren't any data files, create some data.
    fname = "{0}/data_{1}.txt".format(datadir, firstfile + rank)
    if not os.path.isfile(fname):
        create_data(datadir=datadir, firstfile=firstfile, lastfile=lastfile)

    comm.Barrier()  # Rank 0 may still be creating data so wait here.

    sum_thistask = 0  # Initialize.
    N_thistask = 0

    # Now each Task will get its own set of files to read in.
    # This loop ensures each file is only read one.
    for filenr in range(firstfile + rank, lastfile + 1, size):

        fname = "{0}/data_{1}.txt".format(datadir, filenr)
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


def my_example_serial(datadir="./data", firstfile=0, lastfile=11):
    """
    Calculates the mean for numbers across different data files.  Is only run
    on one process to validate the results of `my_example()`.

    If the data files do not exist, creates files containing random numbers.

    Parameters
    ----------

    datadir: String. Default: './data'.
        The directory the data files are located in.

    firstfile, lastfile: Integers.  Default: 0, 11.
        The range of file numbers that are being read.

    Returns
    ----------

    None.
    """

    print("Running my example in serial.")

    # Check to see if the data directory exists.
    if not os.path.exists(datadir) and rank == 0:
        os.makedirs(datadir)

    # If there aren't any data files, create some data.
    fname = "{0}/data_{1}.txt".format(datadir, firstfile)
    if not os.path.isfile(fname):
        create_data(datadir=datadir, firstfile=firstfile, lastfile=lastfile)

    sum_local = 0  # Initialize.
    N_local = 0

    # Now each Task will get its own set of files to read in.
    # This loop ensures each file is only read one.
    for filenr in range(firstfile, lastfile + 1):

        fname = "{0}/data_{1}.txt".format(datadir, filenr)
        data_thisfile = np.loadtxt(fname)

        # Sum up the data from this file.
        sum_local += sum(data_thisfile)
        N_local += len(data_thisfile)

    print("There were {0} values processed with a sum of {1} and mean of {2}"
          .format(N_local, sum_local, sum_local / N_local))


def create_data(datadir="./data", firstfile=0, lastfile=11, N_lower=5e5,
                N_upper=6e5):
    """
    Creates .txt files with a random number of random numbers.  The number of
    files created is lastfile - firstfile + 1.  Used for `my_example()`.

    Parameters
    ----------

    datadir: String. Default: './data'.
        The directory the data files are located in.

    firstfile, lastfile: Integers.  Default: 0, 11.
        The range of file numbers that are being read.

    N_lower, N_upper: Integers.  Default: 5e5, 6e5.
        Generates N random numbers where N_lower < N < N_upper + 1.
        Each random number generated, x_i, is -int(N_lower*3) < x_i < int(N_upper * 3).

    Returns
    ----------

    None.  Data files are created in the `datadir` directory.
    """

    print("Creating data.")

    for filenr in range(firstfile + rank, lastfile + 1, size):
        N = random.randint(N_lower, N_upper + 1)
        data = np.array(random.sample(range(-int(N_lower*3),
                                            int(N_upper*3)), N))

        fname = "{0}/data_{1}.txt".format(datadir, filenr)
        np.savetxt(fname, data)

    print("Done!")


if __name__ == "__main__":

    #hello_world()
    #send_recv()
    #send_recv_mean()
    #reduce_example()
    reduce_array_example()
    #my_example()
    #my_example_serial()
