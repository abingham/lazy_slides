import logging
import urllib.request

from . import flickr


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

def search_photos(tags):
    for tag in tags:
        log.info('searching for images tagged with "{}"'.format(tag))
        photos = flickr.photos_search(tags=tag, per_page=1)
        if not photos:
            log.warning('No results for "{}"'.format(tag))
        else:
            photo = photos[0]
            log.info('found photo: {}'.format(photo))
            yield photo.getURL(size='Medium', urlType='source')

def generate_slides(tags, filenames, outfile):
    outfile.write('\\documentclass{beamer}\n')
    outfile.write('\\usetheme{Copenhagen}\n')
    outfile.write('\\begin{document}\n')
    for tag, filename in zip(tags, filenames):
        outfile.write('\\begin{frame}\n')
        outfile.write('\\frametitle{{{}}}'.format(tag))
        outfile.write('\\begin{center}\n')
        outfile.write('\\includegraphics[]{{{}}}'.format(filename))
        outfile.write('\\end{center}\n')
        outfile.write('\\end{frame}\n')
    outfile.write('\\end{document}\n')

def run():
    tags = ['double deuce', 'monkey', 'herd of llamas']
    urls = search_photos(tags)
    filenames = download(urls)

    with open('slides.beamer', 'w') as outfile:
        generate_slides(tags, filenames, outfile)

if __name__ == '__main__':
    import sys
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout)
    run()
