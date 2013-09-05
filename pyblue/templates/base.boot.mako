<!DOCTYPE html>
<html>
<head>
    <title>
            <%block name="title" />
    </title>
    <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/css/bootstrap-combined.min.css" rel="stylesheet">
</head>
<body>

<div class="container">
    <div class="row">
        <h1>${f.name}</h1>
        <hr>
    </div>

    <div class="row">

            %if f.doctype == "html":
                ${self.body()}
            %elif f.doctype == "markdown" :
                <%block filter="markdown">
                    ${self.body()}
                </%block>
            %elif f.doctype == "asc" :
                <%block filter="asc">
                    ${self.body()}
                </%block>
            %elif f.doctype == "rst" :
                <%block filter="rst">
                    ${self.body()}
                </%block>
            % else :
                <pre>Unexpected doctype: ${f.doctype} </pre>
                ${self.body()}
            %endif

    </div>
</div>


</body>
</html>