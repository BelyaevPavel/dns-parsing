import requests
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from lxml import html

from webapp.models import Category
from webapp.auxiliary import get_next_level_refs


class Command(BaseCommand):
    help = 'Get catalogues titles and references and put into DB'

    def handle(self, *args, **options):
        try:

            headers = {
                'Host': 'www.dns-shop.ru',
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Cache-Control': 'max-age=0'
            }
            catalogue_refs_list = list()
            sess = requests.Session()
            sess.headers.update(headers)
            base_url = 'http://www.dns-shop.ru'
            page = sess.get(base_url)
            root = html.fromstring(page.content.decode('utf-8'))
            top_level_refs_list = [base_url + e.get('href') for e in root.cssselect("ul.catalog a.catalog-icon")]
            # for top_level_ref in top_level_refs_list:
            catalogue_refs_list.extend(
                get_next_level_refs('http://www.dns-shop.ru/catalog/17aa731316404e77/vstraivaemaya-texnika/',
                                    'top-level', sess))
            self.stdout.write(self.style.SUCCESS('catalogue_refs_list filled %s' % len(catalogue_refs_list)))
            for catalogue_ref in catalogue_refs_list:
                try:
                    self.stdout.write(
                        self.style.SUCCESS('entered a cycle %s %s' % catalogue_ref[0], catalogue_ref[1]))
                    c = Category.objects.get(category_name=catalogue_ref[1])
                    self.stdout.write(
                        self.style.SUCCESS('c found'))
                    if c.category_reference != catalogue_ref[0]:
                        category_reference_old = c.category_reference
                        c.category_reference = catalogue_ref[0]
                        self.stdout.write(
                            self.style.SUCCESS('category parameters set'))
                        c.save()
                        self.stdout.write(
                            self.style.SUCCESS('UPDATED: %s %s to %s' % (
                                c.category_name, category_reference_old, c.category_reference)))
                    else:
                        self.stdout.write('ALREADY UP TO DATE: %s %s' % (c.id, c.category_name))
                except ObjectDoesNotExist:
                    c = Category(city_name=catalogue_ref[1], city_id=catalogue_ref[0])
                    c.save()
                    self.stdout.write(
                        self.style.SUCCESS('ADDED: %s %s %s' % (c.id, c.category_name, c.category_reference)))
                except MultipleObjectsReturned:
                    self.stdout.write(
                        self.style.ERROR('Multiple objects were found while searching %s' % catalogue_ref[1]))

            self.stdout.write(self.style.SUCCESS('Successfully filled'))
        except Exception:
            raise CommandError('Something goes wrong')

        self.stdout.write(self.style.SUCCESS('Successfully parsed'))
