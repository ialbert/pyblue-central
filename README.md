Welcome to Pyblue
=================

A simple static site generator. Zero configuration. Works with any existing site.

PyBlue allows the reuse of data and visuals (header/footer) across many pages
and it can generate static sites from dynamic templates.

PyBlue also makes it easy to use [Markdown][markdown] inside of  webpages.

This file is located in <code>docs/index.html</code>
of the <a href="https://github.com/ialbert/pyblue">PyBlue distribution</a>.

Install
-------

Install it with `easy_install pyblue` or `pip install pyblue --upgrade`

Alternatively download it from
the [PyBlue at PyPI](https://pypi.python.org/pypi/pyblue/) site.

**Note:** Version 2.0 of pyblue moved from Mako Templates to Django Templates and
with that introduced other semantic differences. To install
the last version of the `1.*` line use: `easy_install pyblue==1.1.2` or `pip install pyblue=1.1.2`.
See also the docs at: [Pyblue 1.1.2](https://pypi.python.org/pypi/pyblue/1.1.2)

Usage
-----

* Launch pyblue to serve a directory <code>pyblue serve -r docs</code>.
* View your site by visiting <code>http:://localhost:8080</code>.
* Edit your pages and make changes. Reload to page to see your edits.
* Finally, generate static output with: <code>pyblue make -r docs -o html</code>

Documentation
-------------

The [PyBlue documentation][docs-html] was generated with PyBlue itself.

You can also browse the [help in source format][docs-src] for examples.

Licensing
---------

* PyBlue is being developed by Istvan Albert see https://github.com/ialbert
* PyBlue has been inspired by [PyGreen][pygreen] created by Nicolas Vanhoren see https://github.com/nicolas-van
* PyBlue uses the [MIT license][license].

[docs-src]: https://github.com/ialbert/pyblue/tree/master/docs
[docs-html]: http://ialbert.github.io/pyblue/
[django]: https://www.djangoproject.com/
[markdown]: http://en.wikipedia.org/wiki/Markdown
[pygreen]: https://github.com/nicolas-van/pygreen
[license]: https://github.com/ialbert/pyblue/blob/master/LICENSE.txt


