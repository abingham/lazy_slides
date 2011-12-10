import argparse
import logging
import sys
import urllib.request

from . import download
from . import generate
from . import search


log = logging.getLogger(__name__)


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

    urls = search.search_photos(args.tags)
    filenames = download.download(urls)

    with open(args.output, 'w') as outfile:
        generate.generate_slides(args.tags, filenames, outfile)

if __name__ == '__main__':
    run()
