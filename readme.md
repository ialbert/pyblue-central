<h1>Demo Site</h1>
<h2>Development Mode</h2>
<p>Execute:</p>
<pre><code>pyblue -f sites/demo
</code></pre>
<p>Then visit <code>localhost:8080</code> to see the resulting website.
Modify any page for to see a live update of that site.</p>
<h2>Site Generation</h2>
<p>To generate a static version use:</p>
<pre><code>pyblue gen -f sites/demo ~/tmp/demo
</code></pre>
<p>Open the <code>index.html</code> located in the output <code>~/tmp/demo</code> directory.</p>