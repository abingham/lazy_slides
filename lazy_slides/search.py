import logging

from . import flickr


log = logging.getLogger(__name__)

search_function = None

def search_photos(tags):
    for tag in tags:
        log.info('searching for images tagged with "{}"'.format(tag))
        url = search_function(tag=tag)

        if url is None:
            log.warning('No results for "{}"'.format(tag))
        else:
            log.info('found photo: {}'.format(url))

        yield (tag, url)
