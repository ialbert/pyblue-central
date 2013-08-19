<!DOCTYPE html>
<html>
<head>
    <title>
            <%block name="title" />
    </title>
    <link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/css/bootstrap-combined.min.css" rel="stylesheet">
</head>
<body>

<div class="container">
    <div class="row">
        <%block filter="markdown">

            ${self.body()}

        </%block>
    </div>
</div>


</body>
</html>