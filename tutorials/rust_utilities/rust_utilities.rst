=================================
Useful Utilities, Written in Rust
=================================

All these utilities -- plus quite a few more not covered here -- come from `this blog post <https://zaiste.net/posts/shell-commands-rust/>`_, which you may want to check out if any of these seem useful. A common theme of these utilities is that they try to provide a simple, user-friendly interface, with sensible defaults that work for the majority of cases without needing to remember complicated systems of command-line options. They often also take .gitignore files into account if you invoke them from within a Git repository, make automatic use of colored output, and just generally try to provide a slightly higher quality of experience.

``find``-alike, ``fd``
======================
`Link to fd <https://github.com/sharkdp/fd>`_

``fd`` is intended as a modern, simplified ``find`` . Often with ``find`` I just want to search for a file name, or a fragment of a file name. To do that, you need to remember to add the ``-name`` flag, and I *never* remember this because I use ``find`` so infrequently::

    $ find -name my_thesis.tex

With ``fd``, you can just search the way I always expect ``find`` to work::

    $ fd my_thesis.tex

It’s case-insensitive by default, but changes to case-sensitive if the search term contains a capital letter. The search term is treated as a regular expression, so you can use regexes like `‘*.fits’`. It ignores hidden directories and .gitignore patterns if you’re searching in a Git repository (though you can turn this off), and can run commands on the files it finds like ``find`` can.

``sed`` (semi)-alike, ``sd``
============================
`Link to sd <https://github.com/chmln/sd>`_

``sd`` is not *exactly* a replacement for ``sed``, which contains a *lot* of functionality, but it's a replacement for the functionality which 90% of people use ``sed`` for, that of automatically replacing text using regular expressions.

For instance, if you want to convert "The rine in Spine falls minely on the pline," in a file "my_fair_lady_script.txt" to the more comprehensible "The rain in Spain falls mainly on the plain," the necessary ``sed`` command is::

    $ sed -i s/ine/ain/g my_fair_lady_script.txt

The ``-i`` flag performs the substitution in-place in the file (rather than printing it to standard output), the 'g' at the end means to perform the substitution every time the first pattern is found (instead of just the first time per line), and the slashes are just traditional, but required for delineation. For comparison, the equivalent command with ``sd`` is::

    $ sd ine ain test.txt

No need for additional flags, no symbols to delineate the patterns to find and replace, it automatically assumes you want to replace everywhere rather than just the first instance per line. ``sd`` also has familiar features from ``sed`` like capture groups::

    $ echo "123.45" | sd '(?P<dollars>\d+)\.(?P<cents>\d+)' '$dollars dollars and $cents cents'
    123 dollars and 45 cents

Plus other options which make it pretty powerful. ``sd`` doesn't try to duplicate all of ``sed``'s functionality, but focuses on doing the most commonly-used part well.

``grep``-alike, ``ripgrep`` (``rg``)
====================================
`Link to ripgrep <https://github.com/BurntSushi/ripgrep>`_

``ripgrep``, or ``rg`` as the binary is called, is like ``grep``, allowing you to search for text in files. ``rg`` has some nice defaults, like automatically searching directories recursively and printing out line numbers and colored output. With ``grep`` you'd need to do something like::

    $ grep -n -r "some text to find"

while with ``rg`` you can just do::

    $ rg "some text to find"

It supports a lot of the features from ``grep``, while remaining fast when searching Unicode, and can even search for text in some common compressed formats like gzip or lzma.

``grex``
========
`Link to grex <https://github.com/pemistahl/grex>`_

Unlike the first few utilities, ``grex`` isn't a replacement for anything (at least, of any utility I know of). What it does it generate a regular expression from a list of examples you give it which is guaranteed to match those examples. This isn't intended as a replacement for knowing how to write regular expressions (and I still recommend `Regex101 <https://regex101.com/>`_ for complicated regexes, but it can serve as a quick way to get an initial idea of what a regex might need to look like. Here are a few examples from the ``grex`` Github page::

    $ grex a b c
    ^[a-c]$

    $ grex a c d e f
    ^[ac-f]$

    $ grex a b x de
    ^(?:de|[abx])$

       

``tokei``
=========
`Link to tokei <https://github.com/XAMPPRocky/tokei>`_

``tokei`` is a program for quickly counting lines of code on disk and printing out statistics about it. It supports a large number of languages, and while it doesn't have a lot options it can exclude files or directories matching a given pattern, and return either aggregate results per-language (the default) or more granular per-file results. You can sort the output in several ways, such as by language (the default), lines of code, lines of comments, etc., and have it save the output to one of several formats if you want to keep track of changes over time. Here's an example running on the directory where I keep all my code (note that I had to tweak the output format slightly to make a RST table):

``~/code$ tokei``

===================== ======== ============ ============ ============= =============
 Language             Files        Lines         Code     Comments       Blanks
===================== ======== ============ ============ ============= =============
 Python                 91        21042        12452         5374         3216
 ReStructuredText        1           19           13            0            6
 Shell                   1           33           22            7            4
 Plain Text              2           17            0           16            1

 Total                  95        21111        12487         5397         3227
===================== ======== ============ ============ ============= =============

You can exclude directories with the --exclude flag, like so:

``~/code$ tokei --exclude scripts``

=================== ========== ============ =========== =========== ================
 Language            Files        Lines         Code     Comments       Blanks
=================== ========== ============ =========== =========== ================
 Python                 36         6452         3066         2498          888
 ReStructuredText        1           19           13            0            6
 Plain Text              2           17            0           16            1

 Total                  39         6488         3079         2514          895
=================== ========== ============ =========== =========== ================

Or look only in directories called "tests":

``~/code$ tokei */*/tests``

================= =========== ============= ========= ============== ===============
 Language            Files        Lines         Code     Comments       Blanks
================= =========== ============= ========= ============== ===============
 Python                 14         1074          743           89          242

 Total                  14         1074          743           89          242
================= =========== ============= ========= ============== ===============

Showing off the file-specific output:

``~/code$ tokei varconlib/star -f``

===================================== =========== ============= ========== ============ =================
 Language                                 Files        Lines         Code     Comments       Blanks
===================================== =========== ============= ========== ============ =================
 Python                                       4         1755          859          688          208

 varconlib/star/tests/__init__.py                          0            0            0            0
 varconlib/star/__init__.py                                9            1            7            1
 varconlib/star/tests/test_star.py                       160          114           12           34
 varconlib/star/star.py                                 1586          744          669          173

 Total                                        4         1755          859          688          208
===================================== =========== ============= ========== ============ =================

 