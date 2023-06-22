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
formatters = {}

def register_handler(path: str):
    def decorator_handler(func):
        handlers[path] = func
        return func
    return decorator_handler

def register_formatter(func):
    formatters[func.__name__] = func
    return func

@register_formatter
def h1(tag):
    return f"\n === {tag.get_text()} === \n"
    
@register_formatter
def h2(tag):
    return f"\n == {tag.get_text()} == \n"

@register_formatter
def h3(tag):
    return f"\n = {tag.get_text()} = \n"

@register_formatter
def p(tag):
    return tag.get_text()

@register_formatter
def img(_tag):
    return "(Image Omitted)"

def format_post(post):
    soup = BeautifulSoup(post[0]["content"]["rendered"], features="html.parser")
    tags = soup.find_all(["h1", "h2", "h3", "p", "img"])
    return "\n".join(formatters[tag.name](tag) for tag in tags)

@register_handler("/post/{slug}")
def post(request: Request, slug: str):
    post = get(urljoin(wordpress_url, f"wp-json/wp/v2/posts?slug={slug}")).json()
    return format_post(post)

@register_handler("/page/{slug}")
def post(request: Request, slug: str):
    page = get(urljoin(wordpress_url, f"wp-json/wp/v2/pages?slug={slug}")).json()
    return format_post(page)

def handle(request):
    for path, handler in handlers.items():
        parse_result = parse(path, request.path)
        if parse_result is not None:
            return handler(request, **parse_result.named)
    menu = [getenv("HEADER_TEXT")]
    posts = get(urljoin(wordpress_url, "wp-json/wp/v2/posts?filter[posts_per_page]=-1")).json()
    pages = get(urljoin(wordpress_url, "wp-json/wp/v2/pages?filter[posts_per_page]=-1")).json()
    for heading, items, url in (
        ("Pages", pages, "/page/"),
        ("Posts", posts, "/post/")
    ):
        menu.append(f"<==={heading}===>")
        menu += [
            Item(itype=0, path=f"{url}{post['slug']}", text=unescape(post['title']['rendered']), host=request.host, port=request.port)
            for i, post in enumerate(items)
        ]
    return menu

if __name__ == '__main__':
    pituophis.serve("127.0.0.1", int(getenv("PORT")), handler=handle)
