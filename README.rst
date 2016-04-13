Welcome to PyBlue
-----------------

A simple static site generator.

Why another one? There are `many static <https://www.staticgen.com/>`__
site generators already. I found most to be way too complicated, too
many conventions and rules: put this here or there, call it this or
that. It was too tiring to keep up.

PyBlue is different. Everything is optional, nothing is required, use
only what you need. It basically stays out of the way.

Simple things are very easy:

-  No configuration required.
-  Works with any existing site.
-  Easy to include ``markdown``.
-  Easy linking to other pages.
-  Tiny codebase, pyblue is around 500 lines in a single file!

Complicated tasks are easy:

-  PyBlue generates the correct links even if you move pages around.
-  Use `Django
   Templates <https://docs.djangoproject.com/en/1.9/ref/templates/language/>`__
   and all the features that it offers.
-  Easily add data into each page (title, link name, or any arbitrary
   content).

And you can go all the way out if you really want to:

-  Load python modules into each page.
-  Exposed data: database queries, results of online requests etc.
-  Run python code, access and modify data from inside of each page.
-  Extend the Django templates. Add your own ``templatetags``.

Install
~~~~~~~

::

    pip install pyblue --upgrade

Or download it from the `PyBlue at
PyPI <https://pypi.python.org/pypi/pyblue/>`__.

Usage
~~~~~

Launch pyblue to serve a directory

::

    pyblue -r docs

View your site by visiting http:://localhost:8080

Edit your pages and make changes. Reload the page to see your edits
live. Generate static output with:

::

    pyblue -r docs -o html

That's all. Told you it was simple. To see extra help on options run:

::

    pyblue -h

Documentation
~~~~~~~~~~~~~

-  The `PyBlue Documentation <https://ialbert.github.io/pyblue/>`__ was
   generated with PyBlue itself.

You can also browse the `help in source
format <https://github.com/ialbert/pyblue/tree/master/docs>`__ for
examples.

Licensing
~~~~~~~~~

-  PyBlue is being developed by Istvan Albert see
   https://github.com/ialbert
-  PyBlue has been inspired by
   `PyGreen <https://github.com/nicolas-van/pygreen>`__ created by
   Nicolas Vanhoren see https://github.com/nicolas-van
-  PyBlue uses the `MIT
   license <https://github.com/ialbert/pyblue/blob/master/LICENSE.txt>`__.
