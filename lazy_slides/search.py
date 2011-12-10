import logging

from . import flickr


log = logging.getLogger(__name__)

def search_photos(tags):
    for tag in tags:
        log.info('searching for images tagged with "{}"'.format(tag))

        photos = flickr.photos_search(tags=tag, per_page=1)

        if not photos:
            log.warning('No results for "{}"'.format(tag))
            yield (tag, None)
        else:
            photo = photos[0]
            log.info('found photo: {}'.format(photo))
            yield (tag, photo.getURL(size='Medium', urlType='source'))
