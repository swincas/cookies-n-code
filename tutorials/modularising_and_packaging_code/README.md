# Modularising and Packaging Code

This was a tutorial for how any why you should structure your Python code
using modules. 

There are some example scripts in `modularising_code` that share the same functions.
These functions can be extracted and made into a single `utils` (utility) module that
can be imported. This means that you can reuse the same function without having to copy and paste.

There are numerious benafits to this including:
- You can stop copy pasting your own code.
- If you find a bug in one of your functions, you only have to fix it once. Rather than in every script.
- You can build up your own libary of functions and code you use a lot, saving lots of time in the future.
- Makes your scripts much easier to understand if they only contain the code neccesary for what the script is trying to achieve.

---


In `utilspack` I have provided an example of the minimum required to turn a utils.py script into a package
that can be used in all of your projects. It would be a good idea to also include additional files such as a LICENSE,
some tests.


This package can be install in editable mode to your python environment using:
```
pip install -e .
```

Adam Batten, 2021
