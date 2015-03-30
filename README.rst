Welcome to Pyblue
=================

A simple static site generator. Zero configuration. Works with any
existing site.

PyBlue allows the reuse of data and visuals (header/footer) across many
pages and it can generate static sites from dynamic templates.

PyBlue also makes it easy to use
`Markdown <http://en.wikipedia.org/wiki/Markdown>`__ inside of webpages.

This file is located in docs/index.html of the PyBlue distribution.

Install
-------

Install it with ``easy_install pyblue`` or
``pip install pyblue --upgrade``

Alternatively download it from the `PyBlue at
PyPI <https://pypi.python.org/pypi/pyblue/>`__ site.

**Note:** Version 2.0 of pyblue moved from Mako Templates to Django
Templates and with that introduced other semantic differences. To
install the last version of the ``1.*`` line use:
``easy_install pyblue==1.1.2`` or ``pip install pyblue=1.1.2``. See also
the docs at: `Pyblue
1.1.2 <https://pypi.python.org/pypi/pyblue/1.1.2>`__

Usage
-----

-  Launch pyblue to serve a directory pyblue serve -r docs.
-  View your site by visiting http:://localhost:8080.
-  Edit your pages and make changes. Reload to page to see your edits.
-  Finally, generate static output with: pyblue make -r docs -o html

Documentation
-------------

The `PyBlue documentation <http://ialbert.github.io/pyblue/>`__ was
generated with PyBlue itself.

You can also browse the `help in source
format <https://github.com/ialbert/pyblue/tree/master/docs>`__ for
examples.

Licensing
---------

-  PyBlue is being developed by Istvan Albert see
   https://github.com/ialbert
-  PyBlue has been inspired by
   `PyGreen <https://github.com/nicolas-van/pygreen>`__ created by
   Nicolas Vanhoren see https://github.com/nicolas-van
-  PyBlue uses the `MIT
   license <https://github.com/ialbert/pyblue/blob/master/LICENSE.txt>`__.

