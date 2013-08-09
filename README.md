PyBlue
======

A micro web framework/static web site generator.

PyBlue is a simple tool to generate **web based bioinformatics** reports. It has
grown out of the frustrations
experienced while trying share analytical reports with non technical users. LIMS
systems are too difficult to manage, other static blog generators are
too specialized for blogs and can't be easily extended.

It started as a fork of PyGreen: https://github.com/nicolas-van/pygreen later
it has been expanded to include bioinformatics related functionality that warranted
to be split from the original base.

For more information on the original PyGreen module see the `README.pygreen.md` or visit
the PyGreen repository https://github.com/nicolas-van/pygreen.

PyBlue uses the MIT license.

Quick Start
-----------

The tool is currently under development with no releases. To install:

    git clone git@github.com:ialbert/pyblue.git
    cd pyblue
    python setup.py develop

This will locally install the scripts. Now launch a demo server with

    pyblue serve -f sites/basic

Then visit `http://localhost:8080` to see the site. In visit the `pyblue/sites/basic`
folder and look at the content of the files that are then shown in the browser.

What does the tool do?
----------------------

The above command will serve the files located in the specified folder.
Files with the .html extension will be processed by Mako. So if the folder
contains a file index.html with the following code:

    <p>Hello, my age is ${30 - 2}.</p>

When going to http://localhost:8080, you will see:

    <p>Hello, my age is 28.</p>

Generate Site
--------------

PyBlue is meant to export all the files of you current folder
after having the .html files processed by Mako. To do so perform the following:

    blue gen -f input_folder output_folder

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

Extensions
----------

This is where things get interesting.

PyBlue can be used without installing any of these extensions. These are only needed if you happen to work in
specific fields of bioinformatics and you need to generate reports on sequencing data, alignment files, metagenomics
classification etc.

First make sure that your version of python supports the requirments:

    pip install -r requirements.txt

Depending on the reporting that you choose some tools must be present in the system path so that these can
be started directly. For example `samtools` should be launchable from the command line.




