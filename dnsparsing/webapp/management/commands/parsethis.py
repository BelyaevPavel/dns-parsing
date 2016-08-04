import requests
from django.core.management.base import BaseCommand, CommandError
from lxml import html

from webapp.models import Product


class Command(BaseCommand):
    help = 'Get info from desired URL'

    def add_arguments(self, parser):
        parser.add_argument('URL', nargs='+', type=str)

    def handle(self, *args, **options):
        for url in options['URL']:
            try:
                Product.objects.all().delete()
                headers = {
                    'Host': 'www.dns-shop.ru',
                    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Cache-Control': 'max-age=0'
                }
                cookies_dict_perm = {
                    'city_guid_1c': 'a9f47dbf-f564-11de-97f8-00151716f9f5',
                    'current_path': 'e0b5683ebfb7c198073d937c8f22602f83fe9ec2ad7168e4713550d7c4664effa%3A2%3A%7Bi%3A0'
                                    '%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A36%3A%22a9f47dbf-f564-11de-97f8'
                                    '-00151716f9f5%22%3B'
                                    '%7D',
                    'city_path': 'perm'
                }
                cookies_dict_chelyabinsk = {
                    'city_guid_1c': 'b464725e-819d-11de-b404-00151716f9f5',
                    'current_path': '7abc65e7de78550bd204f5adba0ff83a4b445d9cc0d93a137b6840a1695e23cba%3A2%3A%7Bi%3A0'
                                    '%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A36%3A%22b464725e-819d-11de-b404'
                                    '-00151716f9f5%22%3B'
                                    '%7D',
                    'city_path': 'chelyabinsk'
                }
                cookies_dict_zlatoust = {
                    'city_guid_1c': '55506b50-0565-11df-9cf0-00151716f9f5',
                    'current_path': '0b8b9bd1bd5a3d19fca5c9ba8f4b40f31491e335c4d0310582f9e27f70630b95a%3A2%3A%7Bi%3A0'
                                    '%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A36%3A%2255506b50-0565-11df-9cf0'
                                    '-00151716f9f5%22%3B'
                                    '%7D',
                    'city_path': 'zlatoust'
                }

                cookies_dictionaries = [cookies_dict_chelyabinsk, cookies_dict_zlatoust, cookies_dict_perm]
                sess = requests.Session()
                sess.headers.update(headers)
                sess.get('http://www.dns-shop.ru/')
                cookies_dict = requests.utils.dict_from_cookiejar(sess.cookies)
                for k in range(len(cookies_dictionaries)):
                    cookies_dict['city_guid_1c'] = cookies_dictionaries[k]['city_guid_1c']
                    cookies_dict['current_path'] = cookies_dictionaries[k]['current_path']
                    cookies_dict['city_path'] = cookies_dictionaries[k]['city_path']
                    page = sess.get(url=url, cookies=cookies_dict)
                    root = html.fromstring(page.content)
                    product_name_list = [e.text for e in
                                         root.cssselect("div.product div.item-name a.ec-price-item-link")]
                    hreference_list = ['www.dns-shop.ru' + e.get('href') for e in
                                       root.cssselect("div.product div.item-name a.ec-price-item-link")]
                    product_price_list = [e.text for e in
                                          root.cssselect(
                                              "div.product div.item-price span[data-product-param=\"price\"]")]
                    self.stdout.write(cookies_dictionaries[k]['city_path'])
                    for i in range(len(product_name_list)):
                        p = Product(product_name=product_name_list[i], hreference=hreference_list[i],
                                    product_price=product_price_list[i].replace(' ', ''))
                        p.save()
                        self.stdout.write(
                            self.style.SUCCESS(' %s %s %s' % (p.product_name, p.product_price, p.hreference)))
                    self.stdout.write(self.style.SUCCESS('Successfully filled'))
            except Exception:
                raise CommandError('Something goes wrong in %s' % url)

            self.stdout.write(self.style.SUCCESS('Successfully parsed url "%s"' % url))
