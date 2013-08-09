 <%!
    import os, re
 %>

<%def name="hello()">
    Hello world!
</%def>

<%def name="toc(patt='.', root='.', short=True)">
% for name, fname in pygreen.links(patt, root, short=short):
* [${name}](${fname})
% endfor
</%def>

<%def name="link(patt='.', root='.', short=True)">
<%
    links = pygreen.links(patt, root, short=short)
    links = links or [ ("missing", "missing") ]
    name, link  = links[0]
%>[${name}](${link})</%def>


