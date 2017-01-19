import sys, os, urllib
import re
import ssl
context = ssl._create_unverified_context()
ssl._create_default_https_context = ssl._create_unverified_context

from bs4 import BeautifulSoup

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

PROTO="http"
DOMAIN="localhost:4000"

def run(path):
    keep = lambda name: name.endswith(".html")
    patt = re.compile(r'(https?://\S+)')
    seen = set()
    for dirpath, dirnames, fnames in os.walk(path):
        relpath = os.path.relpath(dirpath, start=path)
        #print (relpath)
        fnames = filter(keep, fnames)
        for fname in fnames:
            fpath = os.path.join(dirpath, fname)
            html = open(fpath).read()
            soup = BeautifulSoup(html, "html5lib")
            links = soup.find_all('a')
            for tag in links:
                link = tag.get('href', None)
                if link.startswith("http") or link.startswith('ftp'):
                    continue

                #link = link.replace("../", "")

                if link not in seen:
                    seen.add(link)
                    if link.startswith("http") or link.startswith('ftp'):
                        url = link
                    else:
                        url = f'{PROTO}://{DOMAIN}/{relpath}/{link}'


                    req = Request(url)
                    try:
                        #print (f"{url}")
                        resp = urlopen(req)
                    except Exception as e:
                        print(f'**** Exception {e} for {url} in {relpath}/{fname}')
                    else:
                        #print (f"OK: {url}")
                        data = resp.read(10)


if __name__ == '__main__':
    #url = sys.argv[1]
    path = "/Users/ialbert/book/biostar-handbook/_book"
    run(path)
