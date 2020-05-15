import os
from django.contrib.gis.utils import LayerMapping
from .models import District

district_mapping = {
    'name': 'NAMELSAD',
    'number': 'SLDLST',
    'district_type': 'LSAD',
    'boundaries': 'POLYGON',
}

sldl_shp = '/home/tyler/twoonethree/twoonethree/shapefiles/tl_2016_29_sldl/tl_2017_29_sldl.shp'


def run(verbose=True):
    lm = LayerMapping(District, sldl_shp, district_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)