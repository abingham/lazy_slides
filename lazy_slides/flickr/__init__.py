'''This implements a search method using flickr.com.

This is built on and completely indebted to the work done by James
Clarke on the flickr module contained in this package.
'''

from .flickr import photos_search


def search(tag, count):
    '''Search flickr for photos matching a tag.

    Returns the URL of the first matching photo, or None if no matches
    are found.
    '''

    # TODO: Return up to "count" results.

    photos = photos_search(tags=tag, per_page=count)

    results = []
    for p in photos:
        sizes = p.getSizes()
        sizes.sort(key=lambda size: size['width'], reverse=True)

        results.append(
            p.getURL(
                size=sizes[0]['label'],
                urlType='source'))

    return results
