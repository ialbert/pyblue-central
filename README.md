## Welcome to Pyblue

A simple static site generator.

Why another one? There are [many static](https://www.staticgen.com/) site generators already.

PyBlue is different. Everything is optional.

From the simplest tasks:

- Zero configuration. No really.
- Works with all existing pages.
- Easy `markdown`.
- Easy linking to other pages.
- Tiny codebase, just 400 lines in a single file!

To more complicated:

- Move your pages around. PyBlue will always generate the correct links.
- Full 'Django' templating, headers, footers if you need that.
- Full site customization. Add your own `templatetags`.

Or go all the way out:

- Drop right into python
- Put any type of data into your pages: database queries, results of
  online requests etc.
- Run python code and modify the entire system from
  inside of each page.

### Install

Install it with `easy_install pyblue` or `pip install pyblue --upgrade`

Alternatively download it from
the [PyBlue at PyPI](https://pypi.python.org/pypi/pyblue/) site.

### Usage

* Launch pyblue to serve a directory <code>pyblue serve -r docs</code>.
* View your site by visiting <code>http:://localhost:8080</code>.
* Edit your pages and make changes. Reload the page to see your edits live.
* Finally, generate static output with: <code>pyblue make -r docs -o html</code>

### Documentation

The [PyBlue documentation][docs-html] was generated with PyBlue itself.

You can also browse the [help in source format][docs-src] for examples.

### Licensing

* PyBlue is being developed by Istvan Albert see https://github.com/ialbert
* PyBlue has been inspired by [PyGreen][pygreen] created by Nicolas Vanhoren see https://github.com/nicolas-van
* PyBlue uses the [MIT license][license].

[docs-src]: https://github.com/ialbert/pyblue/tree/master/docs
[docs-html]: http://ialbert.github.io/pyblue/
[django]: https://www.djangoproject.com/
[markdown]: http://en.wikipedia.org/wiki/Markdown
[pygreen]: https://github.com/nicolas-van/pygreen
[license]: https://github.com/ialbert/pyblue/blob/master/LICENSE.txt


