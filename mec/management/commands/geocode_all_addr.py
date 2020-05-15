# requires an instance of pelias running at localhost:4000

import requests
from mec.models import Address
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args, **options):
        ungeocoded = Address.objects.filter(coordinates__isnull=True).filter(city='Maplewood')
        for addr in ungeocoded.iterator():
            self.stdout.write(str(addr))
            response = requests.get(f'http://localhost:4000/v1/search/structured?address="{addr.address1}"&region="{addr.state}"&postalcode="{addr.zip}"').json()
            if len(response['features']) == 1:
                first_result = response['features'][0]
                #postalcode = first_result['properties'].get('postalcode')
                #locality = first_result['properties'].get('locality')
                geocode = first_result['geometry']['coordinates']
                # if postalcode==str(addr.zip):
                #     addr.coordinates=Point(geocode)
                #     addr.save()
                #     self.stdout.write('successful')
                # elif not postalcode:
                #     addr.coordinates=Point(geocode)
                #     addr.save()
                #     self.stdout.write('successful')
                # # elif locality = addr.city
                # else:    
                #     self.stdout.write('failed')
                addr.coordinates=Point(geocode)
                addr.save()
                self.stdout.write('successful')
            else:
                self.stdout.write('failed')
