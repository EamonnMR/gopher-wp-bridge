from os import getenv
from urllib.parse import urljoin
from html import unescape


import pituophis
from pituophis import Item, Request
from requests import get
from parse import parse
from bs4 import BeautifulSoup

wordpress_url = getenv("URL")


handlers = {}

def register_handler(path: str):
    def decorator_handler(func):
        handlers[path] = func
        return func
    return decorator_handler

@register_handler("/post/{id}")
def post(request: Request, id: int):
    post = get(urljoin(wordpress_url, f"wp-json/wp/v2/posts/{id}")).json()
    return BeautifulSoup(post["content"]["rendered"]).get_text()


def handle(request):
    for path, handler in handlers.items():
        parse_result = parse(path, request.path)
        if parse_result is not None:
            return handler(request, **parse_result.named)

    posts = get(urljoin(wordpress_url, "wp-json/wp/v2/posts")).json()

    menu = [
        Item(itype=0, path=f"/post/{post['id']}", text=unescape(post['title']['rendered']), host=request.host, port=request.port)
        for i, post in enumerate(posts)
    ]
    return menu

if __name__ == '__main__':
    pituophis.serve("127.0.0.1", int(getenv("PORT")), handler=handle)

    # Itypes:
    # 0: FILE
    # 1: dir
    # 2: CSO
    # 3: UNKN
    # 4: HQX
    # 5: BIN
    # 6: UUE
    # 7: ?
    # 8: TEL
    # 9: BIN