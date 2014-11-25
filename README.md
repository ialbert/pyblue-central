
<!-- {% load pytags %} -->

Welcome to Pyblue
=================

A simple static site generator. Zero configuration. Works with any existing site.

PyBlue allows the reuse of data and visuals (header/footer) across many pages
and it can generate static sites from dynamic templates.

PyBlue also makes it easy to use [Markdown][markdown] inside of  webpages.

This file is located in <code><a href="https://github.com/ialbert/pyblue/blob/2.0/doc/src/index.html">doc/src/index.html</a></code>
of the <a href="https://github.com/ialbert/pyblue">PyBlue distribution</a>.

Install
-------

Install it with `easy_install pyblue` or `pip install pyblue --upgrade`, or download it from
the [PyBlue at PyPI](https://pypi.python.org/pypi/pyblue/) site.

* Launch pyblue to serve a directory <code>pyblue serve -r docs/src</code>.
* View your site by visiting <code>http:://localhost:8080</code>.
* Edit your pages and make changes. Reload to page to see the effect.
* Finally, generate static output: <code>pyblue gen -r doc/src -o doc/html</code>

Context
-------

The pages are rendered through the Django Template engine.
Users automatically get additional context for each of the pages as
variables that exists.


For example the {% verbatim %}<code>{{ page }}</code>{% endverbatim %} variable is present:

* Writing: {% verbatim %}<code>{{ page.name }}</code>{% endverbatim %} will produce: {{ page.name }}
* Writing: {% verbatim %} <code>{{ page.last_modified }}</code> {% endverbatim %}
  will produce: {{ page.last_modified }}
* Writing: {% verbatim %} <code>{{ page.size|filesizeformat }}</code> {% endverbatim %}
  will produce: {{ page.size|filesizeformat }}

Note how in this last case we also made use of the code>filesizeformat</code> builtin filter from Django.

Users may add more information even load a python module into the page.

Learn {% link "context.html" %}.

Links
-----

To access more advanced features users must add the pyblue tag loader into each page:

{% verbatim %}<code>{% load pytags %}</code>{% endverbatim %}

You can now make use of specific tags for example:

{% verbatim %}<code>{% link "context.html" %}</code>{% endverbatim %} will
produce the following: {% link "context.html" %}.

Why? The {% verbatim %}<code>{% link "context.html" %}</code>{% endverbatim %}
command performs a regular expression search on all files in the directory and
once it finds a match it produces a link to it with the proper path.
This keeps links correct even after moving files! Note how in this
case the file is located in <code>info/context.html</code>

In PyBlue just about every string is used as a regular expression. All a user needs
to specify is the shortest unambiguous part of the file.

Markdown
--------

To include markdown content place it between <code>markdown</code> template tags.

{% code "markdown-example.html" %}

Visit the {% link "markdown-example" %} page.

Include
-------

To include syntax highlighted code write {% verbatim %}<code>{% code "context.py" %}</code>{% endverbatim %}

{% code "context.py" %}

Bootstrap
---------

There are helper methods for bootstrap

Licensing
---------

* PyBlue is being developed by Istvan Albert see https://github.com/ialbert
* PyBlue has been inspired by [PyGreen][pygreen] created by Nicolas Vanhoren see https://github.com/nicolas-van
* PyBlue uses the [MIT license][license].

[django]: https://www.djangoproject.com/
[markdown]: http://en.wikipedia.org/wiki/Markdown
[pygreen]: https://github.com/nicolas-van/pygreen
[license]: https://github.com/ialbert/pyblue/blob/master/LICENSE.txt

