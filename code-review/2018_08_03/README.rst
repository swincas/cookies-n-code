=======================================================
Running a jupyter-notebook remotely (on a compute node)
=======================================================

Step 1:
"""""""
ssh into remote host (ozstar):

.. code:: bash

  ssh myusername@ozstar.hpc.swin.edu

Check whether jupyter-notebook exists by running:

.. code:: bash

  which jupyter-notebook

If the command returns something like:

*jupyter-notebook: Command not found.*

then you might want to either do a "conda install jupyter-notebook" if conda is already available, or add **one** of the following:

.. code:: bash
  
  module load ipython/5.5.0-python-2.7.14
  module load ipython/5.5.0-python-3.6.4

to your .bashrc file, depending on which python version you prefer. You can do "source ~/.bashrc", or simply exit the remote prompt and ssh back for this to take effect.


Step 2:
"""""""
Request an interactive node with some resources using the srun wrapper, sinteractive:

.. code:: bash

  sinteractive --time=01:00:00 --mem=2GB

This will request 1 cpu with 2 GB of RAM with a walltime of 1 hour for your jupyter-notebook session.

When the resources are allocated, you will be returned a command prompt on the compute node that you've been granted. Note the name of the compute node by running:

.. code:: bash
  
  echo $HOST

This should return something like: john32


Step 3:
"""""""

Start a jupyter-notebook server but without a browser by running the following command:

.. code:: bash

  jupyter-notebook --no-browser --ip=$HOST

The "--ip=$HOST" flag specifies that the notebook server will listen on johnXX IP address rather than localhost.

If the server successfully launches, it should print something like:

*The Jupyter Notebook is running at:*

*http://john32:8888/?token=hf7hjbakd93bd92n497hdfn203nf*

Note the port number that the server binds to (8888 in this case), let's call it the *remote_port*, as we're going to use it in the next step.

Step 4:
"""""""

In a new terminal, ssh into ozstar, but this time using the port forwarding flag:

.. code:: bash

  ssh myusername@ozstar.hpc.swin.edu -L local_port:host:remote_port

replacing *remote_port* by what was given in step 3 (8888 in this example), and *host* by what was given in step 2. For simplicity, let's make *local_port=remote_port*.

Finally, launch your favorite browser, copy/paste the address that the jupyter-notebook is running at, as given in step 3, and replace the host name in the address ("john32" in this case) by "localhost". In case *local_port!=remote_port*, replace the *remote_port* number in the address by the *local_port* that you've selected.
