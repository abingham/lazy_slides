import logging
import urllib


log = logging.getLogger(__name__)

def download(urls):
    for idx, url in enumerate(urls):
        filename = 'slide_image_{}.jpg'.format(idx)
        log.info('Downloading {} to {}'.format(
                url, filename))

        with urllib.request.urlopen(url) as infile:
            with open(filename, 'wb') as outfile:
                outfile.write(infile.read())

        yield filename
