***********************************************
Introduction to Python decorators and factories
***********************************************

In Python, it may sometimes be useful to apply a specific operation on several function/class definitions.
Think for example about reusing the same docstring several times throughout a Python package, or wanting to register all function names in a global list.
In the first case, it would be inconvenient to have to copy/paste the same docstring snippet over and over again, especially when you want to make a change to it later on (and you realize you used it over 100 times).
However, Python has a solution to this problem: **decorators** and **factories**.

What are decorators?
********************
A Python decorator is any callable object (usually a function) that takes a function/class definition as its sole input argument, performs one or several operations on it and returns a similar definition with added functionality.
So, the most basic decorator one could write would be:

.. code:: python

    def my_decorator(func):
        return(func)

This decorator simply takes a function definition and returns it immediately, without modifying it.
For this reason, it does not really have a purpose, but it does show the absolute basic structure of a decorator.

Decorators can be applied to a function/class definition by using the ``@`` marker in Python.
Let's define a test function first (it returns the sum of the two input arguments):

.. code:: python

    def test(a, b):
        return(a+b)

The decorated version of this function would look like:

.. code:: python

    @my_decorator
    def test(a, b):
        return(a+b)

Whenever Python encounters the use of a decorator, it provides the function/class definition it is used on to the decorator and assigns what is returned as the new definition.
Therefore, using a decorator in this way is the same as executing:

.. code:: python

    def test(a, b):
        return(a, b)
    test = my_decorator(test)

Examples of decorators
**********************
The decorator from before had no functionality at all, as it simply returned the definition that was provided to it.
Here, I introduce two different types of decorators: wrapper and attribute.

Wrapper decorators
------------------
A wrapper decorator is a decorator that modifies the inputs and outputs of a definition.
It does this by creating a new definition within the decorator call that uses the original definition, but changes the way it is used in.
The basic structure of a decorator that modifies the returned object of a definition is as follows:

.. code:: python

    def my_decorator(func):
        def do_nothing(*args, **kwargs):
            return(func(*args, **kwargs))
        return(do_nothing)

This decorator takes a function definition as ``func``, saves its definition locally and returns a function ``do_nothing``.
When called, ``do_nothing`` simply calls the local ``func`` with all input arguments and returns its output.
Therefore, in essence, this decorator does not have any functionality.

However, we can change this.
Let's say that we want a decorator that adds 1 to the output of a function.
Then the decorator would look like this:

.. code:: python

    def add_one(func):
        def do_adding(*args, **kwargs):
            return(func(*args, **kwargs)+1)
        return(do_adding)

If we now use this decorator on our test function from before:

.. code:: python

    @add_one
    def test(a, b):
        return(a+b)

Then the following will be true:

.. code:: python

    >>> test(2, 6)
    9

What happened here is that our decorator ``add_one`` returned a function definition ``do_adding``, which calls the original ``func``, adds 1 to its output and then returns it.
For that reason, the answer will be 9.

It is also possible to modify the input of our test function.
For example, let's say that we want input argument ``b`` to always be equal to 1.
Then, we can achieve this by using the following decorator (as the input is now modified, the decorator cannot be generalized):

.. code:: python

    def set_b_unity(func):
        b = 1
        def new_func(a):
            return(func(a, b))
        return(new_func)

Using this on our test function in the same way as before, will give us a function definition ``test(a)``.
The ``b`` input argument can no longer be provided, as we set it to unity within the decorator.
Using our new test function will give:

.. code:: python

    >>> test(2)
    3
    >>> test(5)
    6
    >>> test(2, 6)
    TypeError: new_func() takes 1 positional argument but 2 were given

Here, we can see that the modified test function will raise an error if we provide more than one input argument.
However, we can also see something else happening.
The error message mentions the function ``new_func()``, while our function was called ``test()``.
The reason for this is because we basically overrode the ``test()`` function and replaced it with ``new_func()``.

Obviously, this is not really desirable, as this also means that the docstring of the original ``test()`` function no longer exists and it shows quite clearly that the function was decorated.
But, Python has a decorator (irony) to avoid this, called ``functools.wraps`` (although it will still not show the proper name in error messages).
Using this decorator on ``new_func()`` will copy all important properties from ``func()`` to ``new_func()``, making it look like it is the original definition.

So, we would have to modify both our decorators to:

.. code:: python

    from functools import wraps

    def add_one(func):
        @wraps(func)
        def do_adding(*args, **kwargs):
            return(func(*args, **kwargs)+1)
        return(do_adding)
 
    def set_b_unity(func):
        b = 1
        @wraps(func)
        def new_func(a):
            return(func(a, b))
        return(new_func)

Now, our test function will correctly display its name and docstring.
However, be aware that using ``wraps()`` in a decorator that modifies the inputs may lead to confusing situations, as the original docstring probably still mentions all input arguments the function originally took.

Attribute decorator
-------------------
Whereas a wrapper decorator modifies the inputs and outputs of a definition, an attribute decorator directly modifies the attributes of one without wrapping it.
A simple example of an attribute decorator would be a decorator that sets the name of a definition to ``'hello'``:

.. code:: python

    def set_name(func):
        func.__name__ = 'hello'
        return(func)

    @set_name
    def test(a, b):
        return(a+b)

    >>> test.__name__
    'hello'

As you can see here, the decorator returns the original function after modifying one of its attributes (its name), unlike a wrapper decorator which returns a new definition.

Attribute decorators can have many different uses, just like wrapper decorators.
Remember that I mentioned that decorators can be used for copy/pasting docstrings into definitions?
One could for example write a decorator that can substitute docstring snippets into the docstring of a definition.
Below is a shortened version of the ``docstring_substitute`` decorator in my `e13Tools package <https://github.com/1313e/e13Tools/blob/bb83a26ed892adc73bf8f6a7cce6d946cee87652/e13tools/utils.py#L128>`_:

.. code:: python

    # Define custom decorator for substituting strings into a function's docstring
    def docstring_substitute(*args, **kwargs):
        # Check if solely args or kwargs were provided
        if len(args) and len(kwargs):
            raise InputError("Either only positional or keyword arguments are "
                             "allowed!")
        else:
            params = args or kwargs

        # This function performs the docstring substitution on a given definition
        def do_substitution(target):
            # Check if target has a docstring that can be substituted to
            if target.__doc__:
                # Perform docstring substitution
                target.__doc__ = target.__doc__ % (params)

            # Raise error if target has no docstring
            else:
                raise InputError("Target has no docstring available for "
                                 "substitutions!")

            # Return the target definition
            return(target)

        # Return decorator function
        return(do_substitution)

Let's say that we want to substitute the line ``'Hello'`` into the docstring of our test function.
We could do this quite easily in the following way:

.. code:: python

    doc = 'Hello'

    @docstring_substitute(doc=doc)
    def test(a, b):
        """
        %(doc)s
        %(doc)s
        """
        return(a+b)

The docstring of our test function will now have ``'Hello'`` twice, as can be seen by checking its docstring attribute:

.. code:: python

    >>> test.__doc__
    '\n    Hello\n    Hello\n    '

This decorator would allow one to write a description of a very common input argument in a package once, save it somewhere and substitute it into every function/class definition it is required in.
Not only would this make your descriptions consistent, it also saves you a lot of trouble if you ever want to change the description.
(If you are interested, my e13Tools package has two other docstring decorators: one for copying the entire docstring of a function to another one and an other for appending a docstring to another.)

Stacking decorators
*******************
In some cases, it might be necessary to use more than just a single decorator on a definition.
For example, let's assume that we want to use our previous ``add_one`` decorator with a new ``double`` decorator (doubles the output) on our test function:

.. code:: python

    from functools import wraps

    def add_one(func):
        @wraps(func)
        def do_adding(*args, **kwargs):
            return(func(*args, **kwargs)+1)
        return(do_adding)

    def double(func):
        @wraps(func)
        def do_doubling(*args, **kwargs):
            return(func(*args, **kwargs)*2)
        return(do_doubling)

    @add_one
    @double
    def test(a, b):
        return(a+b)

This will return a function definition ``test()`` which has both decorators applied to it.
In most cases, the order in which the decorators are applied does not matter, as they do not influence the same part of the definition.
In this case however, both decorators influence the outcome of the function and therefore the order is important.

If we would use this new definition as ``test(2, 6)``, we should get either 17 or 18, depending on the order in which the decorators are applied.
Think about which answer should be correct and why.

Executing this will give us:

.. code:: python

    >>> test(2, 6)
    17

Now, take a moment to think about why the answer is 17 and not 18.

The reason for this can basically be found in the explanation of decorators above.
Whenever a decorator is used, it takes the definition found right below it and returns a new definition.
Therefore, the ``double`` decorator is applied first, which returns a new definition unto which the ``add_one`` decorator is applied.
So, decorators are always applied from the bottom.
As I have shown before, the application of these decorators could also be written as:

.. code:: python

    def test(a, b):
        return(a+b)

    # Option 1
    test = double(test)
    test = add_one(test)
    
    # Option 2
    test = add_one(double(test))

As many decorators can be applied to the same definition as you want, and you can also stack the same decorator multiple times.
Keep in mind though that stacking wrapper decorators means that calling the resulting definition will go through every single applied decorator and may make your code slower.

As you probably noticed, ``wraps()`` and ``docstring_substitute()`` are 'decorators' that take an input argument first.
This is because they are actually **decorator factories**, which I will explain below.

Decorator factories
*******************
A decorator factory is a function that takes input arguments, saves them locally and returns a decorator definition.
In essence, it is a special type of **function factory**, which I will explain later.
In the case of the ``wraps()`` and ``docstring_substitute()`` decorator factories, one first provides it with the information on what is being wrapped or what should be substituted.
It then returns an attribute decorator that will use the provided input when the decorator is used on a definition.

For attribute decorators, it is quite common that they are provided by decorator factories.
However, one can also perfectly make a wrapper decorator factory.
For example, let's say that we want to use ``add_one``, but instead of applying it as many times as needed, we want a decorator that simply adds whatever number we want to the output.
This can be done with a decorator factory:

.. code:: python

    from functools import wraps

    def add_x(x):                           # Decorator factory
        def add_decorator(func):            # Decorator
            @wraps(func)
            def do_adding(*args, **kwargs): # Wrapper function
                return(func(*args, **kwargs)+x)
            return(do_adding)
        return(add_decorator)

    @add_x(5)
    def test(a, b):
        return(a+b)

Using the ``add_x()`` decorator factory, we have generated a decorator that always adds 5 to the output of our test function.
It will now give us:

.. code:: python

    >>> test(2, 6)
    13

As before, the application is as follows (where the decorator is generated first and then applied):

.. code:: python

    def test(a, b):
        return(a+b)

    test = add_x(5)(test)

Function/class factories
************************
The decorator factories I have shown above, are special types of **function factories**.
As mentioned before, a function factory is a function that takes a set of input arguments, stores them locally and returns a function definition (or a class definition for class factories).
Function factories other than decorator factories are usually only used in special situations, and you will probably not commonly encounter one.
However, that does not mean they are not useful.

Whenever any definition is called, it has access to all input arguments that were provided to it (called **locals**) and all variables available in the namespace of the definition (called **globals**).
Anything higher than the scope of this definition (so, the namespace in which it exists) has no access to the locals, while anything lower sees all locals as globals.
The following will explain this a bit better, where I use comments to indicate what the globals and locals are in specific scopes:

.. code:: python

    var1 = 0

    # globals contains all Python builtins
    # locals contains var1

    def test(var2):
        # globals contains builtins and var1
        # locals contains var2
        pass

    def test2(var3):
        # globals contains builtins and var1
        # locals contains var3
        pass

    def factory(var4):
        # globals contains builtins and var1
        # locals contains var4
        def test3(var5):
            # globals contains builtins, var1 and var4
            # locals contains var5
            pass
        return(test3)
 
Whenever a scope exits (like, a function returns), all corresponding pointers to its locals are lost.
If Python detects that an object has no pointers anymore, it will remove it from memory.
However, this is where the usefulness of function factories comes in.

In the example given above, ``var4`` is a local variable to ``factory()``, but a global variable to ``test3()``.
As ``test3()`` is returned by the function factory, it is necessary for ``var4`` to be available.
For that reason, Python makes a special local environment for the ``test3()`` function such that ``var4`` can be accessed (you can check this for yourself by looking at the namespace of the returned function).
But, this environment is only available to the ``test3()`` function.
As the scope of the user is outside the function factory after calling it, the user itself will only have access to the builtins and ``var1``.
Therefore, this makes the ``var4`` variable private to the ``test3()`` function, and to my knowledge, this is the only way to make something as close to private as possible in Python (it can actually still be accessed from the outside, although this is incredibly hard).

So, what is the benefit of this?
For example, we could rewrite our ``set_b_unity`` decorator from before to a proper function factory that allows for default values to be set:

.. code:: python

    def get_default_b_test(b):
        def test(a, b=b):
            return(a+b)
        return(test)

The code here is very similar as before, but it also has a few differences.
By using a function factory, we were able to set a default value for ``b`` (which is not possible with decorators).
Now, when executing ``get_default_b_test(5)``, we will get a ``test(a, b)`` function that by default has its ``b`` set to 5.

However, imagine that you have a function that when called once, should always be called with the exact same value for a specific input argument every single time it is called in this process.
This can be done very quickly by simply removing the input argument ``b`` from ``test(a, b)`` in the definition above:

.. code:: python

    def get_static_b_test(b):
        def test(a):
            return(a+b)
        return(test)

``get_static_b_test(5)`` will now return ``test(a)`` with ``b`` automatically set to 5 and nobody can change it.

Doing so can have a few benefits.
Depending on what kind of functions you are using, it might be necessary to check the validity of the input arguments.
If the user always has to provide the same value anyways, it is kind of pointless to validate that input argument every time the function is called, which might take quite some time to do.
Plus, it is annoying that the user has to provide it the entire time.
By using a function factory and validating the input value for ``b``, it would allow you to check it once, and never having to do that again.
And, it also becomes impossible for the user to accidentally provide a different value later on, as the created function does not take that input argument.

The same principle can be applied to class factories, where one wants to provide the same input argument(s) to the initialization of a class every time.
Also note that all wrapper decorators are essentially function factories themselves.
