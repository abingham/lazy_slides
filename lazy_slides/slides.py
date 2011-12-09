import argparse
import logging
import sys
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

def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument(
        'tags', metavar='T', type=str, nargs='+',
        help='A tag on which to search and generate a slide.')
    parser.add_argument(
        '-V, --verbose', dest='verbose', action='store_true',
        help='Generate extra output.')
    parser.add_argument(
        '-o, --output',
        dest='output',
        #action='store_const',
        default='slides.beamer',
        metavar='F',
        help='The filename for the output.')

    return parser.parse_args()

def init_logging(verbose):
    if verbose:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    logging.basicConfig(
        level=level,
        stream=sys.stdout)

def run():
    args = parse_args()
    init_logging(args.verbose)

    urls = search_photos(args.tags)
    filenames = download(urls)

    with open(args.output, 'w') as outfile:
        generate_slides(args.tags, filenames, outfile)

if __name__ == '__main__':
    run()
