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

## Link generation macros

## url directly in HTML
<%def name="link(name)"><% link, name = p.link(f, name) %><a href="${link}">${name}</a></%def>

## url with rst syntax
<%def name="rst_link(name)"><% link, name = p.link(f, name) %>`${name} <${link}>`_</%def>

<%def name="path(name)"><% link, name = p.link(f, name) %>${link}</%def>

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

<%def name="include(fname, start='', end='')">
<%
	import os, string, itertools, re
	fpath = os.path.join(p.folder, fname)
	lines = map(lambda x: x.strip("\n"), file(fpath))
	if start:
		lines = itertools.dropwhile(lambda x: not re.search(start, x), lines)
	if end:
		lines = itertools.takewhile(lambda x: not re.search(end, x), lines)
	code = "\n".join(lines)
%>
<pre class="prettyprint">
${code.decode('utf-8')}
</pre>
</%def>

## called it source initially kept it for backwards compatibility
## will be removed later
<%def name="source(fname, start='', end='')">
<%
	import os, string, itertools, re
	fpath = os.path.join(p.folder, fname)
	lines = map(lambda x: x.strip("\n"), file(fpath))
	if start:
		lines = itertools.dropwhile(lambda x: not re.search(start, x), lines)
	if end:
		lines = itertools.takewhile(lambda x: not re.search(end, x), lines)
	code = "\n".join(lines)
	print ("""!!! the source('%s') pyblue command has been deprecated please use include('%s') instead""" %(fname, fname))
%>
<pre class="prettyprint">
${code.decode('utf-8')}
</pre>
</%def>

<%def name="execute(cmd)">
<%
	import subprocess as s
	import os
	saved = os.getcwd()
	os.chdir(p.folder)
	pop = s.Popen(cmd, shell=True, stdout=s.PIPE, stderr=s.PIPE, close_fds=True)
	(c_out, c_err ) = (pop.stdout, pop.stderr)
	os.chdir(saved)
%>
<pre>${c_err.read()}
${c_out.read()}</pre>
</%def>