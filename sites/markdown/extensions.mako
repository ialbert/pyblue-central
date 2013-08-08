 <%!
    import os
 %>

<%def name="hello()">
    Hello world!
</%def>

<%def name="toc()">
% for fname in pygreen.files:
* [${fname}](${fname})
% endfor
</%def>


