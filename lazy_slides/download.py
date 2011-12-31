import logging
import os
import urllib
from urllib.parse import urlparse
import uuid


log = logging.getLogger(__name__)

def download(url):
    '''Download a file specified by a URL to a local file.

    This generates a unique name for the downloaded file and saves
    into that.

    :param url: The URL to download.
    '''

    parsed = urlparse(url)

    # Calculate the save-file name
    filename = os.path.split(parsed.path)[1]
    filename_comps = os.path.splitext(filename)
    filename = '{}_{}{}'.format(
        filename_comps[0],
        uuid.uuid4(),
        filename_comps[1])

    log.info('Downloading {} to {}'.format(
            url, filename))

    # Save the URL data to the new filename.
    with urllib.request.urlopen(url) as infile:
        with open(filename, 'wb') as outfile:
            outfile.write(infile.read())

    return filename
