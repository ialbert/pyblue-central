
import mistune, re
from mistune import escape
from mistune import HTMLRenderer

YOUTUBE_PATT = re.compile(r'https?://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([^&\s]+)')
TWITTER_PATT= re.compile(r'https?://(www\.)?twitter\.com/.+/status/(\d+)')


class LocalRenderer(HTMLRenderer):

    def link(self, text, url, title=''):

        match_youtube = YOUTUBE_PATT.match(url)
        match_twitter = TWITTER_PATT.match(url)

        if match_youtube:
            video_id = match_youtube.group(3)
            embed_link = f'https://www.youtube.com/embed/{video_id}'
            return f'<iframe width="560" height="315" src="{embed_link}" frameborder="0" allowfullscreen></iframe>'
        elif match_twitter:
            return f'<blockquote class="twitter-tweet"><a href="{url}"></a></blockquote>'

        else:
            attr = ' rel="nofollow"'
            title = escape(title, quote=True)
            text = escape(text, quote=True)
            return f'<a href="{url}" title="{title}" {attr}>{text}</a>'
            #return super().link(text, url, title)

    def block_text(self, text):
        print ("text:", text)
        return super().block_text(text)

markdown = mistune.create_markdown(
    renderer=LocalRenderer(),
    plugins=['url']
)


text = """

# Hello World

(my link https://www.psu.edu)

[<zoom>](https://www.psu.edu "is the best <hey>")

`$hey$`
 
Here is @foo and @bar
 
<ok>boomer

https://www.youtube.com/watch?v=jNQXAC9IVRw

https://twitter.com/username/status/1234567890'

---

"""


html = markdown(text)

print (html)
