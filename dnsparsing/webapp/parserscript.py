from lxml import html, etree
from lxml.etree import fromstring
from cssselect import GenericTranslator, SelectorError
import requests

# request cookies: CASSESSION=0944df38e164c4f3c7d0f47549fbcaeb; city_guid_1c=a9f47dbf-f564-11de-97f8-00151716f9f5; city_path=perm; current_path=e0b5683ebfb7c198073d937c8f22602f83fe9ec2ad7168e4713550d7c4664effa%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A36%3A%22a9f47dbf-f564-11de-97f8-00151716f9f5%22%3B%7D; rerf=AAAAAFecwU68/28kA9sGAg==; ipp_uid2=WXG16ZKRFA3DTTXG/TD92pocxgSJdQB8nHujMIg==; ipp_uid1=1469890894310; _ga=GA1.2.1336302220.1469890895; _ym_uid=1469890896345276709

headers = {
    'Host': 'www.dns-shop.ru',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cache-Control': 'max-age=0'
}
sess = requests.Session()
sess.headers.update(headers)
page = sess.get('http://www.dns-shop.ru/catalog/17a89b1a16404e77/tyunery-dlya-kompyutera/')
root = html.fromstring(page.content)
product_name_list = [e.text for e in root.cssselect("div.product div.item-name a.ec-price-item-link")]
hreference_list = ['www.dns-shop.ru' + e.get('href') for e in
                   root.cssselect("div.product div.item-name a.ec-price-item-link")]
product_price_list = [e.text for e in root.cssselect("div.product div.item-price span[data-product-param=\"price\"]")]
for i in range(len(product_name_list)):
    print 'i = %i name = %s ref = %s price = %s' % (i, product_name_list[i], hreference_list[i], product_price_list[i])
