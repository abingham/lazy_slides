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
        'tags', metavar='KEYWORD', type=str, nargs='+',
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
    parser.add_argument(
        '-F, --fail-on-missing',
        dest='fail_on_missing',
        action='store_true',
        help='Fail when a tag generates no matches.')

    return parser.parse_args()

def init_logging(verbose):
    if verbose:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    logging.basicConfig(
        level=level,
        stream=sys.stdout)

def main():
    args = parse_args()
    init_logging(args.verbose)

    urls = search.search_photos(args.tags)

    def filter_failures(match):
        if match[1] is None:
            if args.fail_on_missing:
                raise ValueError(
                    'No matching images for tag "{}"'.format(
                        match[0]))
            else:
                return False
        return True
    urls = list(filter(filter_failures, urls))

    tags = (u[0] for u in urls)
    urls = (u[1] for u in urls)

    filenames = download.download(urls)

    with open(args.output, 'w') as outfile:
        generate.generate_slides(tags, filenames, outfile)

if __name__ == '__main__':
    run()
