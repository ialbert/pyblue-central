Welcome to Pyblue
=================

A simple static site generator. Zero configuration. Works with any existing site.

PyBlue allows the reuse of data and visuals (header/footer) across many pages
and it can generate static sites from dynamic templates.

PyBlue also makes it easy to use [Markdown][markdown] inside of  webpages.

This file is located in <code><a href="https://github.com/ialbert/pyblue/tree/master/docs/src/index.html">docs/src/index.html</a></code>
of the <a href="https://github.com/ialbert/pyblue">PyBlue distribution</a>.

Install
-------

Install it with `easy_install pyblue` or `pip install pyblue --upgrade`, or download it from
the [PyBlue at PyPI](https://pypi.python.org/pypi/pyblue/) site.

* Launch pyblue to serve a directory <code>pyblue serve -r docs/src</code>.
* View your site by visiting <code>http:://localhost:8080</code>.
* Edit your pages and make changes. Reload to page to see the effect.
* Finally, generate static output: <code>pyblue gen -r doc/src -o doc/html</code>

Documentation
-------------

* PyBlue ready [source format][docs-src]
* PyBlue generated [html format][html-src]

Licensing
---------

* PyBlue is being developed by Istvan Albert see https://github.com/ialbert
* PyBlue has been inspired by [PyGreen][pygreen] created by Nicolas Vanhoren see https://github.com/nicolas-van
* PyBlue uses the [MIT license][license].

[docs-src]: https://github.com/ialbert/pyblue/tree/master/docs/src/
[docs-html]: https://github.com/ialbert/pyblue/tree/master/docs/html/index.html
[django]: https://www.djangoproject.com/
[markdown]: http://en.wikipedia.org/wiki/Markdown
[pygreen]: https://github.com/nicolas-van/pygreen
[license]: https://github.com/ialbert/pyblue/blob/master/LICENSE.txt


