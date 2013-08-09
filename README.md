PyBlue
=======

A micro web framework/static web site generator.

PyBlue is a simple tool to generate web based bioinformatics reports. It has grown out of the frustrations
experienced while trying share analytical reports with non technical users.

It started as a fork of PyGreen: https://github.com/nicolas-van/pygreen and
it has been expanded to include bioinformatics related functionality. See
the README.pygreen.md or see the PyGreen repository https://github.com/nicolas-van/pygreen
for more details on PyGreen

PyBlue uses the MIT license.

Quick Start
-----------

The tool is currently under development with no releases. To install:

    git clone git@github.com:ialbert/pyblue.git
    python setup.py develop

To launch and serve files:

    pyblue serve -f inputfolder

The above command will serve the files located in the specified folder.
Files with the .html extension will be processed by Mako. So if the folder
contains a file index.html with the following code:

    <p>Hello, my age is ${30 - 2}.</p>

When going to http://localhost:8080, you will see:

    <p>Hello, my age is 28.</p>

Generate Site
--------------

PyGreen can also export all the files of you current folder after having the .html files processed by
Mako. To do so, type this command:

    blue gen -f inputfolder <output_folder>

This can be useful to post your files on Github Pages or any other free static files hosting services.

Files with the .mako or .py extension will not be visited by `pyblue gen`.
This is useful to avoid generating macros files or templates to inherit.
This also applies to hidden files.

Templates
---------

There are default templates included in the `templates` folder. These will be automatically included in
the template search path. To override them create identically named templates in your site's root folder.

See this template https://github.com/ialbert/pyblue/blob/master/sites/markdown/index.html
as an example of what is included in the defaults.

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




