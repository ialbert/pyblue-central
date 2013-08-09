 <%!
    import os, re
 %>

<%def name="hello()">
    Hello world! ${self.name}
</%def>

<%def name="links(patt='.', rel='.')">
<ul class="links">
% for name, link in pygreen.links(patt, rel):
<li> <a href="${link}">${name}</a> </li>
% endfor
</ul>
</%def>

