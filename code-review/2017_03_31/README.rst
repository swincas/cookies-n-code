Why use make
--------------

- automates compilations for code, LaTeX docs
- tracks dependencies and (re)compiles as necessary
- parallel compilation (also serves as a bug check on the Makefile)

Writing a Makefile
--------------------

``make`` needs rules to specify three things:

1. what is the ``target`` 
2. what are the ``pre-requisites`` to make the ``target``
3. how to create the ``target`` once all the `pre-requisites` are met

Anatomy of a Makefile
----------------------

1. Macros contain variable names. For instance, ``SRC := main.c utils.c`` is a macro
2. Targets are specified by a ``:``. For instance, ``all: MYEXE`` specifies the target ``all``
3. Names that follow the ``:`` are pre-requisites. (Left of the ``:`` are targets, right of the ``:`` are pre-reqs). ``MYEXE`` was the pre-req in the previous line.
4. Line following the ``target`` specifies the rule to create the target based on the pre-reqs. This rule **MUST** be initialized by a new-line followed by a ``<TAB>``, like so

:: 

  MYEXE: prereq1 prereq2 
  <TAB> $(CC) -o MYEXE prereq1 prereq2

5. It is considered bad practice to repeat names, so the in the real-world the previous line would be written as

::

  OBJS := prereq1 prereq2   # OBJS is a macro
  MYEXE: $(OBJS)
  <TAB> $(CC) -o $@ $(OBJS)
    
where, ``$@`` is a special ``make`` variable that contains the name of the target, ``$(OBJS)`` contains the names of all your object files, ``$(CC)`` is your compiler. 

**note** Targets that are not a file, should be declared as ``.PHONY`` (for instance, ``all``, ``clean``). Otherwise, if a file called ``all`` or ``clean`` exists in the directory, ``make`` will not do anything.


C/C++/Fortran Compile Conventions
----------------------------------
- ``CFLAGS/CPPFLAGS/FCFLAGS`` is automatically picked from the environment by the compiler to create the object file
- ``LDFLAGS`` is used during linking to produce the final shared/static library or executable.
- ``-lgsl`` is short-hand for a file called ``libgsl.so`` somewhere in the ``LD_LIBRARY_PATH``, similarly, ``-lm`` is short-hand for ``libm.so`` (that contains all your standard math)


Basic Makefile
--------------
There is a basic `Makefile <Makefile_BASIC>`_ already in the repo, you can use that for simple single directory jobs that will only run on linux. This Makefile should be sufficient for all (small) personal code-bases.


Important Makefile tricks and Compile Flags
-------------------------------------------

- Automatically pick up where ``GSL`` is located by using ``gsl-config --prefix``
- Embed library paths into the executable by using the compiler flag ``-Xlinker -rpath -Xlinker /path/to/the/library``. 

For instance:
::
    GSL_DIR := $(shell gsl-config --prefix)
    GSL_CFLAGS := $(shell gsl-config --cflags)
    GSL_LIBS := $(shell gsl-config --libs)
    GSL_LIBDIR := $(GSL_DIR)/lib

    MYEXE: $(OBJS)
    <TAB> $(CC) -o $@ $(OBJS) $(GSL_LIBS) -Xlinker -rpath -Xlinker $(GSL_LIBDIR)

With this extra flag, your exectuable will **always** pick up the compile time library, **irrespective of your runtime environment**. You can completely eliminate the runtime error of ``library not found``. 





