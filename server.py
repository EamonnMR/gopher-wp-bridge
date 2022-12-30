from os import getenv
from urllib.parse import urljoin
from html import unescape

import pituophis
from pituophis import Item
from requests import get

wordpress_url = getenv("URL")

def handle(request):
    posts = get(urljoin(wordpress_url, "wp-json/wp/v2/posts")).json()

    menu = [
        Item(itype=1, path="/" + post['slug'], text=unescape(post['title']['rendered']), host=request.host, port=request.port)
        for post in posts
    ]
    print(menu)
    return menu

if __name__ == '__main__':
    pituophis.serve("127.0.0.1", int(getenv("PORT")), handler=handle)
