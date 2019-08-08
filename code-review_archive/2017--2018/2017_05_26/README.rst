MPI in Python
--------------

===============
mpi4py on g2
===============

Load the ``mpi4py`` package like so:

-  module purge
-  module load mpi4py
-  module list

::

     Currently Loaded Modulefiles:
     1) openmpi/x86_64/gnu/1.6.1-psm             3) blas/x86_64/gnu/3.2.1-4
     5) scipy-numpy-dependencies/x86_64/gnu/1.0  7) mpi4py/x86_64/gnu/1.3
     2) atlas/x86_64/gnu/3.8.4-2                 4) lapack/x86_64/gnu/3.2.1-4
     6) python/2.7.2                    


=============================
MPI "Hello World" with mpi4py
=============================

.. code:: python

    #!/usr/bin/env python
    # -*- encoding: utf-8 -*-

    from __future__ import print_function
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    name = MPI.Get_processor_name()

    print("Hello, World! I am MPI task {0} of {1} on {2}".format(rank, size, name))

===========================
Running the previous script
===========================

Assumes you have loaded the ``mpi4py`` package

::

    mpirun -np 4 python hello.py

============================
Further examples of mpi4py
============================


- https://github.com/jbornschein/mpi4py-examples
- https://coco.sam.pitt.edu/~emeness/wp-content/uploads/2013/11/introMPIwithMPI4Py.pdf

=======================================
Convenient Wrapper over OpenMP and MPI
=======================================

If you tend to run embarrassingly parallel jobs, then you can use
a ``pool`` to map **independent** tasks onto cores. Each core then works
on its own task in parallel. ``emcee`` uses such a pool to run MCMC chains
either on a single node (OpenMP) or on multiple nodes of a cluster (MPI)

- https://github.com/adrn/schwimmbad
- https://github.com/dfm/emcee

