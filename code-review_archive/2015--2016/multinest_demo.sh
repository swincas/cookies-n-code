#!/bin/bash

# If pymultinest can't find the multinest library then run the python script
# through this file. Make sure you modify it so it points to your multinest
# installation directory.
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/bekos/usr/local/multinest/lib/ python ./multinest_demo.py
