 <%!
    import os, re
 %>

<%def name="hello()">
    Hello world! ${self.name}
</%def>

<%def name="toc(patt='.', rel='.')">
% for name, fname in pygreen.links(patt, rel):
* [${name}](${fname})
% endfor
</%def>

<%def name="links(patt='.', rel='.')">
<ul class="links">
% for name, link in pygreen.links(patt, rel):
<li> <a href="${link}">${name}</a> </li>
% endfor
</ul>
</%def>

