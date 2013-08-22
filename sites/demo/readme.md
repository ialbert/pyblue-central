
Demo Site
=========

Development Mode
-----------------

Execute:

    pyblue -f sites/demo

Then visit `localhost:8080` to see the resulting website.
Modify any page for to see a live update of that site.

Site Generation
---------------

To generate a static version use:

    pyblue gen -f sites/demo ~/tmp/demo

Open the `index.html` located in the output `~/tmp/demo` directory.