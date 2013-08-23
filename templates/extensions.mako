## file unindented so that can be used for Markdown
<% import os %>

<%def name="hello()">
Hello world!
</%def>

<%def name="toc(tag=None, match=None)">
<ul class="toc">
%for link, name in p.toc(f, tag=tag, match=match):
<li><a href="${link}">${name}</a></li>
%endfor
</ul>
</%def>


<%def name="link(name)"><% link, name = p.link(f, name) %><a href="${link}">${name}</a></%def>


<%def name="gallery(tag=None, match=None, span=4)">
<ul class="thumbnails">
%for link, name in p.toc(f, tag=tag, match=match, is_image=True):
<li class="span${span}">
<a href="${link}" class="thumbnail">
<img src="${link}" alt="${name}">
</a>
</li>
%endfor
</ul>
</%def>

<%def name="source(fname)">
<%
	import os
	fpath = os.path.join(p.folder, fname)
%>
<pre>
%for line in file(fpath):
	${line.strip("\n")}
%endfor
</pre>
</%def>