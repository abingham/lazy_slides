from .flickr import photos_search


def search(tag):
    '''Search flickr for photos matching a tag.

    Returns the URL of the first matching photo, or None if no matches
    are found.
    '''

    photos = photos_search(tags=tag, per_page=1)
    if not photos:
        return None
    return photos[0].getURL(size='Medium', urlType='source')
