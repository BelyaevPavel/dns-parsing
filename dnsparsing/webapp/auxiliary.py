from lxml import html, etree
from lxml.etree import fromstring
import cssselect
import requests


def get_next_level_refs(reference, category_title, sess):
    category_refs_list = list()
    p = sess.get(reference)
    print(category_title)
    r = html.fromstring(p.content.decode('utf-8'))
    next_level_refs_list = ['http://www.dns-shop.ru' + e.get('href') for e in
                            r.cssselect("div.category-items-desktop a.category-item-desktop")]
    next_level_category_names_list = [e.text for e in r.cssselect(
        "div.category-items-desktop a.category-item-desktop span.category-title")]
    if len(next_level_category_names_list) == 0 & len(next_level_refs_list) == 0:
        return [[reference, category_title]]
    else:
        for i in range(len(next_level_refs_list)):
            category_refs_list.extend(
                get_next_level_refs(next_level_refs_list[i], next_level_category_names_list[i], sess))
        return category_refs_list