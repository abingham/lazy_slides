'''This implements image search for bing.
'''

import logging

from simple_bing import SimpleBing

log = logging.getLogger(__name__)

app_id = 'EEC00CEB4CA13F1AE6F9F1244B67304D527884A0'

def search(tag, count):
    bing = SimpleBing(app_id)
    response = bing.search(query=tag,
                           sources='image',
                           image_count=count)

    results = response['SearchResponse']['Image']['Results']

    if not results:
        return None

    return [r['MediaUrl'] for r in results]
