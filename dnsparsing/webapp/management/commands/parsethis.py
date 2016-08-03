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
                page = requests.get(url)
                root = html.fromstring(page.content)
                product_name_list = [e.text for e in root.cssselect("div.product div.item-name a.ec-price-item-link")]
                hreference_list = ['www.dns-shop.ru' + e.get('href') for e in
                                   root.cssselect("div.product div.item-name a.ec-price-item-link")]
                product_price_list = [e.text for e in
                                      root.cssselect("div.product div.item-price span[data-product-param=\"price\"]")]
                for i in range(len(product_name_list)):
                    p = Product(product_name=product_name_list[i], hreference=hreference_list[i],
                                product_price=product_price_list[i].replace(' ', ''))
                    p.save()
                    self.stdout.write(self.style.SUCCESS(
                        'i = %i name = %s ref = %s price = %s' % (i, p.product_name, p.hreference, p.product_price)))
                self.stdout.write(self.style.SUCCESS('Successfully filled'))
            except Exception:
                raise CommandError('Something goes wrong in %s' % url)

            self.stdout.write(self.style.SUCCESS('Successfully parsed url "%s"' % url))
