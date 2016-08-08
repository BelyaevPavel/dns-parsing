import requests
from django.core.management.base import BaseCommand, CommandError
from lxml import html

from webapp.models import City


class Command(BaseCommand):
    help = 'Get info from desired URL'

    #    def add_arguments(self, parser):
    #        parser.add_argument('URL', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            City.objects.all().delete()
            headers = {
                'Host': 'www.dns-shop.ru',
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Cache-Control': 'max-age=0'
            }

            sess = requests.Session()
            sess.headers.update(headers)
            page = sess.get('http://www.dns-shop.ru/ajax/region-nav-window/')
            root = html.fromstring(page.content)
            city_id_list = [e.get('data-city-id') for e in root.cssselect("ul.cities a")]
            city_name_list = [e.text for e in root.cssselect("ul.cities a")]
            for i in range(len(city_name_list)):
                c = City(city_name=city_name_list[i], city_id=city_id_list[i])
                c.save()
                self.stdout.write(self.style.SUCCESS('%s %s %s' % (c.city_id, c.city_name, c.id)))
            self.stdout.write(self.style.SUCCESS('Successfully filled'))
        except Exception:
            raise CommandError('Something goes wrong')

        self.stdout.write(self.style.SUCCESS('Successfully parsed'))
