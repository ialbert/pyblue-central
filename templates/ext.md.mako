<%!
    import utils
%>

<%def name="hello()">
    Hello world!
</%def>

<%def name="gallery(root='.')">
<%
    files = pygreen.links(root=root)
    files = filter(lambda x: x[1].endswith("png"), files)
%>
<div style="clear:both;">
% for name, fname in files:
<div style="float:left; width:260px;">
<a href="${fname}"><img width="250px" src="${fname}" /></a>
</div>
% endfor
</div>

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


