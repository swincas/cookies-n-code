# Spectral Cubes 
Author: Lydia Haacke

## What does this presentation cover?
KCWI spectral cube analysis with Python and [QFitsView](https://www.mpe.mpg.de/~ott/dpuser/qfitsview.html). Check out the [fix_kcwi_cubes](fix_kcwi_cubes.py) file for the Python side of things. It is highly recommended that you utilise the recording of the live presentation for a better understanding of QFitsView, so please get in touch with the CnC organisers to get access.

If people want to follow along it requires quite a bit of setup, but just in case, here's instructions. There are multiple parts to the presentation, so it's not necessary to do everything.

#### Part 1 (viewing cubes):
- have a spectral cube downloaded on your computer somewhere
- have QFitsView installed (available from Swinburne Self Service)

#### Part 2 (rebinning and stacking cubes):
- have two spectra cubes you want to add in a directory with nothing else. Bonus points if it is KCWI cubes
- create a python environment with [montagepy](https://pypi.org/project/MontagePy/)
- save the file that is attached somewhere accessible on your laptop
- We'll go over how to create the file to actually run this during the session