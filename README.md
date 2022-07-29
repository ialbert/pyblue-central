## Welcome to PyBlue

A simple static site generator developed many eons ago (2013) when writing static site generators was still cool. (As of 2022 some features are still better than all the alternatives)

### Why another one static generator?

There are so [many static](https://www.staticgen.com/) site generators already.

Alas I found most options to be way too complicated. 

Each has many conventions and rules: you have to put this here, you have to put that there, many naming convention. It was too tiring to keep up.

Then as I was developing courses over the years I found that I could not easily reorganize the site, the links would all break when I moved files around. Very annoying.

Finally when I wanted to do something complicated like running a piece of code while generating the site the tools could
not do it.

At some point I realized that I'll just have to roll my own, and I did, and here it is.

PyBlue is different. Everything is optional, nothing is required, use only what you need. It basically stays out of the way.

Simple things are very easy:

- No configuration required.
- Works with any existing site.
- Easy to include `markdown`.
- Easy linking to other pages.
- Tiny codebase, pyblue is around 500 lines in a single file!

Complicated tasks are easy:

- PyBlue generates the correct links even if you move pages around.
- Use [Django Templates][django_templates] and all the features that it offers.
- Easily add data into each page (title, link name, or any arbitrary content).

And you can go all the way out if you really want to:

- Load python modules into each page.
- Exposed data: database queries, results of online requests etc.
- Run python code, access and modify data from inside of each page.
- Extend the Django templates. Add your own `templatetags`.

### Documentation

* The [PyBlue Documentation][docs-html] was generated with PyBlue itself.

You can also browse the [help in source format][docs-src] for examples.

### Install

    pip install pyblue --upgrade

Or download it from the [PyBlue at PyPI](https://pypi.python.org/pypi/pyblue/).

### Usage

Launch pyblue to serve a directory

    pyblue -r docs

View your site by visiting http:://localhost:8080

Edit your pages and make changes. Reload the page to see your edits live.
Generate static output with:

    pyblue -r docs -o html

That's all. Told you it was simple. To see extra help on options run:

    pyblue -h

### Licensing

* PyBlue is being developed by Istvan Albert see https://github.com/ialbert
* PyBlue has been inspired by [PyGreen][pygreen] created by Nicolas Vanhoren see https://github.com/nicolas-van
* PyBlue uses the [MIT license][license].

[docs-src]: https://github.com/ialbert/pyblue-central/tree/master/docs
[docs-html]: https://ialbert.github.io/pyblue-central/
[django]: https://www.djangoproject.com/
[markdown]: https://en.wikipedia.org/wiki/Markdown
[pygreen]: https://github.com/nicolas-van/pygreen
[license]: https://github.com/ialbert/pyblue/blob/master/LICENSE.txt
[django_templates]: https://docs.djangoproject.com/en/1.9/ref/templates/language/

