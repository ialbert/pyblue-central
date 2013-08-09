<%namespace name="x" file="ext.md.mako" inheritable="True"/>

<!DOCTYPE html>
<html>
<head>
    <title>
        <%block name="title" />
    </title>
</head>
<body>

<%block filter="markdown">

    ${self.body()}

</%block>

</body>
</html>