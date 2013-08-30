Welcome to PyBlue
=================

**PyBlue** provides a simple way to generate static files used to present data analysis reports, personal webpages,
static blogs etc.

Features
--------

* zero configuration, **PyBlue** requires no settings or initialization for existing sites
* minimalistic design with a tiny codebase of around 350 lines of Python
* add one line to each HTML file turn on the functionality of the extension modules
* supports Markdown based content
* simple linking to all content within site
* supports table of contents and galleries
* optional tagging or grouping files with regular expression patterns
* uses python [Mako templates][mako] which means that there are no limitations to what you can do ;-)

**PyBlue** is a modification of the [PyGreen project][pygreen]
that is being expanded to include more data oriented functionality.

Demo Sites
----------

Main demonstration site:

 * [PyBlue Demo][demo]

Other sites:

* [Personal homepage of Istvan Albert](http://www.personal.psu.edu/users/i/u/iua1/)
* [Bioinformatics Consulting Center at PSU][bcc]

Installation
------------

Requirements: [setuptools](https://pypi.python.org/pypi/setuptools/1.0) needs to be installed.

The software is currently under development and is released via GitHub. To install you can
[download the archive](https://github.com/ialbert/pyblue/archive/master.zip)  or clone via `git`:

    git clone git@github.com:ialbert/pyblue.git

Once you obtained the source code install with:

    cd pyblue
    python setup.py install

This will install the `pyblue` script.

Quick Start
-----------

Launch a demo server with

    pyblue serve -f sites/demo

Then visit `http://localhost:8080` to see the site. Look in the `sites/demo`
folder to see the sources that create the site.

To generate a static version of the site into the `~/tmp/www/` folder type:

    pyblue gen -f sites/demo ~/tmp/www


What does the tool do?
----------------------

**PyBlue** generates static sites. Typically this involves two steps.

1. Serving the file during the site development. **PyBlue** will serve
   the files from a directory and presents the latest
   version of the file. This allows the site creator to
   write the site and check continuously what the output will look like.

2. Once the site is ready to be published the site generation
   command can be used to create a static copy of the site in the desired folder.
   The files in the output folder can be distributed and can be opened in a browser
   if stored on the local filesystem or they can be served via a static web-server such as
   apache, nginx etc.


Templates
---------

Files with the `.html` extension will be processed via [Mako templates][mako]. For example
if the folder contains a file `index.html` with the following code:

    <p>Hello, my age is ${30 - 2}.</p>

When going to `http://localhost:8080`, you will see:

    <p>Hello, my age is 28.</p>

Visit the [Mako templates][mako] site to see the full power of the templating system.

Context
--------

**PyBlue** allows embedding metadata into the files as Mako comments. For example adding
the text below into an html file sets the name, a sort order (used to order listings)
and the tags (used to group files) of the page:

    ##name Home Page
    ##sortkey 1
    ##tags home intro
    ##foo bar

Any meta tag added to the page may be later retrieved in the page via the default variable `f`
(current file) context variable: `${f.foo}`.
This makes it really easy to add navigation bars and breadcrumbs with location specific
rendering. See the [PyBlue Demo][demo] site for examples.

Extensions
----------

**PyBlue** offers functions that can be used to generate tables of contents or
galleries. See the [PyBlue Demo][demo] site for examples.
for details:

    # generate a table of contents
    ${toc()}

    # generate a table of contents for
    # the pages tagged as 'data'
    ${toc(tag='data')}

The `sites/demo` folder contain numerous examples on the usage.

Generating Site
---------------

**PyBlue** can export all the files of the input folder
after having the `.html` files processed by Mako. To do so perform the following:

    pyblue gen -f input_folder output_folder

Then look at the `output_folder`.

Hidden files or those with the .mako or .py, extension will not be visited by `pyblue gen`.
This is useful to avoid generating macros files or templates to inherit.

Note that the `gen` command will also create all sub-folders. Only files
under a certain size will be copied automatically
(this is to avoid copying potentially large files back and forth).
To copy large files set up a separate synchronization script.
Note that the relative links will still work.

Templates
---------

There are default templates included in the `templates` folder. These will be automatically included in
the template search path. To override them create identically named templates in your site's root folder.

View the default templates in the [source code][pyblue]

Example Sites
-------------

There are a number of [example sites][sites] included in the `sites` folder.

You may serve/generate each site independently to see what they contain.
These sites demonstrate the utility functions that are included with **PyBlue** and the default templates. For example:
generating tables of content, matching and displaying links with certain properties.

Advanced Functionality
----------------------

PyBlue may be **minimalistic** but it is not **simplistic**. It supports an easy embedding of any
template context into the template.

Adding a `settings.py` python module into the root of the site will make that module accessible
within the template context under the variable `p.settings`. What this means is that you can run any type
of python based code and then expose it later within the template context.

For example suppose that one wants to query sample information from a database. Place the python
query to the database in the `settings.py` module and then return that in the template.
For example a `settings.py` module could contain:

    def query():
        results = "<some python code goes here>"
        return results

Then every single template that is created could access the results of that code via:

    p.settings.query()

Inserting the content of another file can be performed with `source("demo.py")`
Note that the `source` command can also take parameters such as `start` and `end`.
When those are set only the region that is between the matching regular expressions
will be included.

Capturing the output of running a program would be achieved via `execute("python demo.py")`

Licensing
---------

**PyBlue** is built on [PyGreen][pygreen] created by [Nicolas Vanhoren](https://github.com/nicolas-van)

**PyBlue** is being developed by [Istvan Albert](https://github.com/ialbert)

**PyBlue** uses the MIT license.

[mako]: http://www.makotemplates.org/
[demo]: http://bcc.bx.psu.edu/pyblue/demo/
[bcc]: http://bcc.bx.psu.edu
[iua]: http://www.personal.psu.edu/users/i/u/iua1/
[rza]: http://www.personal.psu.edu/users/i/u/iua1/
[pygreen]: https://github.com/nicolas-van/pygreen
[sites]: https://github.com/ialbert/pyblue/blob/master/sites/
[pyblue]: https://github.com/ialbert/pyblue/
