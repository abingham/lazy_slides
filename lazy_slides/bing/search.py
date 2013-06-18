'''This implements image search for bing.
'''

import logging

from .bing_search_api import BingSearchAPI

log = logging.getLogger(__name__)

key = '654ANTd4Y2O6HjQoWkvqnw757tXRyZI+mDnPVpNzjJY'

def search(tag, count):
    my_key = key
    query_string = tag
    bing = BingSearchAPI(my_key)
    params = {# 'ImageFilters':'"Face:Face"',
              '$format': 'json',
              '$top': count,
              '$skip': 0}
    rslt = bing.search('image',query_string,params).json() # requests # 1.0+
    images = rslt['d']['results'][0]['Image']
    return [r['MediaUrl'] for r in images]
    # Also, width, height, etc.


def main():
    from lazy_slides import download
    x = search('llama', 10)
    print(download.download(x[0], '.'))

if __name__ == '__main__':
    main()
