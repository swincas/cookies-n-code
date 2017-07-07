# Using Python virtual environments

## With anaconda

`conda create --name <handy name> [python=2 or 3] [libraries to install]`

Example:

`conda create --name astrowork python=2 matplotlib numpy pandas astropy`

Then activate with:

`source activate astrowork`

Installing libraries into the virtual environment:

`conda install <lib>` if avaliable, else `pip install <lib>`

When you're done:

`source deactivate`

Installing libraries of particular versions:

`pip install astropy=1.2`

You can also specify ranges and limits on versions.

Installing a bunch of libraries from a file:

`pip install -r requirements.txt`

## Using python virtuelenv

First:

`pip install virtualenv`

Then navigate to where you want it to live, e.g.:

`cd work/astroproj`

Create the venv:

`virtualenv astroenv`

And to switch to the environment:

`source astroenv/bin/activate`

Install libraries with `pip`, and to escape the venve - `deactivate`.
