Python basics
--------------

===========
List
===========

.. code:: python

  my_list = []
  my_list = [1,2,3,4,'blabla']

Add an element to a list:

.. code:: python

  a.append(1)

Access an element at index *i*

.. code:: python

  a[i]

===========
Dictionary
===========

.. code:: python

  my_dict = {}
  my_dict = {key1:val2, key2:val2, ...}

  my_dict['key'] = val

  for key in my_dict.keys():
      print (key, my_dict[key])

============================================
Read and write file using 'with'
============================================

Avoid closing the file using with:

.. code:: python

    # Open file in read mode:
    # the file closes automatically at the end of the with block
    with open('filename.csv', 'r') as f_in:
        for line in f:
            if "someword" in line:
                # do something
                pass
            print line.split(',')

    # Open the file in write mode, and create it if it doesn't exist:
    # create a csv file type output:
    with open('filename.csv', 'w+') as f_out:
        f_out.write('something,something_else,last_thing\n')

    # Open the file in append mode:
    # Will continue writing at the end
    with open('filename.csv', 'a') as f_out:
        f_out.write('some_more,more_else,more_last_thing\n')


=====================================================
Use Pandas' read_csv to read csv file to data frame
=====================================================

.. code:: python

  from pandas import read_csv
  df = read_csv('filename.csv')

  print (df['something'])

  # For numerical columns, min, max, mean, ...
  df['timing'].min()
  df['ratio'].unique()

  # Apply constraints to print only rows of interest:
  df.loc[(df['ratio'] == 5) & (df['flux'] == 2000)]

======================
ipython (console)
======================

Auto reload externally loaded files:

.. code:: python

  %load_ext autoreload
  %autoreload 2

Paste code copied onto memory from somewhere else:

.. code:: python

  %paste
  %cpaste

======================
jupyter notebook
======================

Show figures inline:

.. code:: python

  %matplotlib inline
  %config InlineBackend.figure_format='retina'