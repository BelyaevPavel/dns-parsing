# coding: utf-8
import requests
from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError
from lxml import html

from webapp.models import Product, City


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

                sess = requests.Session()
                sess.headers.update(headers)
                sess.get('http://www.dns-shop.ru/')
                cookies_dict = requests.utils.dict_from_cookiejar(sess.cookies)
                city_list = City.objects.filter(
                    Q(city_name__exact='Челябинск') | Q(city_name__exact='Магнитогорск') | Q(
                        city_name__exact='Екатеринбург') | Q(city_name__exact='Пермь') | Q(
                        city_name__exact='Сургут') | Q(
                        city_name__exact='Тюмень') | Q(city_name__exact='Курган'))
                for city in city_list:
                    cookies_dict['city_guid_1c'] = city.city_id
                    page = sess.get(url=url, cookies=cookies_dict)
                    root = html.fromstring(page.content)
                    aux_names_and_refs = root.cssselect("div.product div.item-name a.ec-price-item-link")
                    product_name_list = [e.text for e in aux_names_and_refs]
                    hreference_list = ['www.dns-shop.ru' + e.get('href') for e in aux_names_and_refs]
                    product_price_list = [e.text for e in
                                          root.cssselect(
                                              "div.product div.item-price span[data-product-param=\"price\"]")]
                    self.stdout.write(city.city_name)
                    for i in range(len(product_name_list)):
                        p = Product(product_name=product_name_list[i], hreference=hreference_list[i],
                                    product_price=product_price_list[i].replace(' ', ''))
                        p.save()
                        self.stdout.write(
                            self.style.SUCCESS(' %s %s %s' % (p.product_name, p.product_price, p.hreference)))
                    self.stdout.write(self.style.SUCCESS('Successfully filled'))
            except Exception:
                raise CommandError('Something goes wrong while processing %s.' % url)

            self.stdout.write(self.style.SUCCESS('Successfully parsed url "%s"' % url))
