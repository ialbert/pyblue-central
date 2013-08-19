PyBlue
======

A micro web framework/static web site generator.

PyBlue is a simple tool to generate static sites to distribute **data analysis** reports. It has
grown out of the frustrations experienced while trying share analytical reports
with non technical users. Laboratory information management systems are
too difficult to install, maintain and manage. Yet at the same time the typical
static blog generators are too specialized for blogging
and can't be easily extended to support non-blog domains of applications.

PyBlue started out as a fork of PyGreen: https://github.com/nicolas-van/pygreen
it is being expanded to include more bioinformatics related functionality and
that warranted to be split from the original base.

For more information on the original PyGreen module see the `README.pygreen.md` or visit
the PyGreen repository https://github.com/nicolas-van/pygreen.

Sites running PyBlue
--------------------

 * http://bcc.bx.psu.edu
## * http://www.personal.psu.edu/iua1/

PyBlue uses the MIT license.

Quick Start
-----------

The tool is currently under development and is released via GitHub. To install:

    git clone git@github.com:ialbert/pyblue.git
    cd pyblue
    python setup.py develop

This will locally install the scripts. Now launch a demo server with

    pyblue serve -f sites/demo

Then visit `http://localhost:8080` to see the site. In visit the `pyblue/sites/basic`
folder and look at the content of the files that are then shown in the browser.

What does the tool do?
----------------------

The above command will serve all the html files located in the specified folder.
Files with the .html extension will be processed by Mako. So if the folder
contains a file index.html with the following code:

    <p>Hello, my age is ${30 - 2}.</p>

When going to http://localhost:8080, you will see:

    <p>Hello, my age is 28.</p>

Extensions
----------

PyBlue allows embedding metadata into the files as Mako comments. For example the listing below will
mark the file with meta data for the name, its sort order key and tags:

    ##name Home Page
    ##sortkey 1
    ##tags home intro

Any metatag may be added and later retrieved in the page.

Special functions may be used to generate tables of contents.

   # generate a table of contents
   ${p.toc()}

   # generate a table of contents for
   # the pages tagged as 'data'
   ${p.toc(tag='data')}

The `sites/demo` and `sites/docs` folders contain numerous examples on the usage.

Generate Site
--------------

PyBlue is meant to export all the files of you current folder
after having the .html files processed by Mako. To do so perform the following:

    pyblue gen -f input_folder output_folder

Then look at the `output_folder`.

Hidden files or those with the .mako or .py, extension will not be visited by `pyblue gen`.
This is useful to avoid generating macros files or templates to inherit.

Templates
---------

There are default templates included in the `templates` folder. These will be automatically included in
the template search path. To override them create identically named templates in your site's root folder.

See the basic templates at https://github.com/ialbert/pyblue/blob/master/sites/
for examples of what is included in the default extensions.

Example Sites
-------------

There are a number of example sites included in the `sites` folder.

You may serve/generate each site independently to see what they contain.

These sites demonstrate the utility functions that are included in PyBlue and the default templates. For example:
generating tables of content, matching and displaying links with certain properties.




