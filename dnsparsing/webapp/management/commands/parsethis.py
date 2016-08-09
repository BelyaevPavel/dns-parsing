import requests
from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from lxml import html

from webapp.models import Product, City, Category


class Command(BaseCommand):
    help = 'Get info from desired URL'

    # def add_arguments(self, parser):
    #    parser.add_argument('URL', nargs='+', type=str)

    def handle(self, *args, **options):
        # for url in options['URL']:

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
        # self.stdout.write(self.style.SUCCESS('sess started'))
        cookies_dict = requests.utils.dict_from_cookiejar(sess.cookies)
        # self.stdout.write(self.style.SUCCESS('cookies set'))
        try:
            city_list = City.objects.filter(check=True)
            category_list = Category.objects.filter(check=True)
        except Exception:
            raise CommandError('Something goes wrong while searching')
        self.stdout.write(self.style.SUCCESS('all found'))
        if len(city_list) != 0:
            for city in city_list:
                self.stdout.write(city.city_name)
                for category in category_list:
                    self.stdout.write(category.category_name)
                    cookies_dict['city_guid_1c'] = city.city_id
                    page = sess.get(url=category.category_reference, cookies=cookies_dict)
                    root = html.fromstring(page.content)
                    for product in root.cssselect("div.product"):
                        name = product.cssselect("div.item-name a.ec-price-item-link")
                        if not name:
                            continue
                        name = name[0]
                        ref = name.get('href')
                        name = name.text
                        price = product.cssselect(
                            "div.product div.item-price span[data-product-param=\"price\"]")
                        if not price:
                            continue
                        price = float(price[0].text.replace(' ', ''))
                        self.stdout.write(
                            self.style.SUCCESS('Parameters set %s %s %s' % (name, city, category)))
                        p, created = Product.objects.get_or_create(product_name=name, city=city,
                                                                   category=category)
                        self.stdout.write(self.style.SUCCESS('get or create succeed'))
                        if not created:
                            # self.stdout.write(self.style.SUCCESS('not created'))
                            if p.product_price != price or p.hreference != ref:
                                # self.stdout.write(self.style.SUCCESS('something changed'))
                                price_old = p.product_price
                                p.product_price = price
                                hreference_old = p.hreference
                                p.hreference = ref
                                p.save()
                                self.stdout.write(
                                    self.style.SUCCESS(
                                        'UPDATED: %s %s -> %s\n%s -> %s' % (
                                            p.product_name, price_old, p.product_price, hreference_old,
                                            p.hreference)))
                            else:
                                self.stdout.write('ALREADY UP TO DATE: %s %s' % (p.id, p.product_name))
                        else:
                            self.stdout.write(self.style.SUCCESS('created'))
                            p.product_price = price
                            p.hreference = ref
                            p.category = category
                            p.save()
                            self.stdout.write(
                                self.style.SUCCESS('ADDED: %s %s' % (p.product_name, p.product_price)))

                    self.stdout.write(self.style.SUCCESS('Successfully filled'))
        else:
            self.stdout.write('No city was selected')

        self.stdout.write(self.style.SUCCESS('Successfully parsed url'))
