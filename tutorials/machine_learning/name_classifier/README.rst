============================================================
Build a classification model to predict the gender of a name
============================================================

Author: Wael Farah

Year: 2019

Training set:
"""""""""""""
male_names.txt

female_names.txt

To create model:
""""""""""""""""
.. code:: bash

  python create_model.py

This will create a new directory called "model", where the random forest classifier will be placed

To predict the gender:
""""""""""""""""""""""
.. code:: bash

  python predict_gender.py INPUT_NAME

where INPUT_NAME is a name of your choice
