Markdown Example
================
{% load pytags %}

This file is pure markdown file with `.md` extension.

Processing rules:

* It will be rendered via the `markdown-base.html` parent template.
* Users can overide this with an identically named template in their project folder.
* To make use of the pyblue specific extensions the template must include the `load pytags` section.

Back to home: {% link "index.html" %}