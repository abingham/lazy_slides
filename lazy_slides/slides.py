import argparse
import importlib
import logging
import sys
import urllib.request

from . import download
from . import generate
from . import manipulation
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
    parser.add_argument(
        '-s, --search-function',
        dest='search_function',
        default='lazy_slides.flickr.search',
        metavar='FUNCTION',
        help='The Python function used to search for images URLs.')

    return parser.parse_args()

def init_logging(verbose):
    if verbose:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    logging.basicConfig(
        level=level,
        stream=sys.stdout)

def init_search_function(search_function):
    from . import search

    toks = search_function.split('.')
    module_name = '.'.join(toks[:-1])
    func_name = toks[-1]

    mod = importlib.import_module(module_name)

    search.search_function = getattr(mod, func_name)

def main():
    args = parse_args()
    init_logging(args.verbose)
    init_search_function(args.search_function)

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

    tags = [u[0] for u in urls]
    urls = [u[1] for u in urls]

    filenames = list(download.download(urls))

    for filename in filenames:
        manipulation.resize(filename, filename, (300, 300))

    log.info('Writing output to file {}'.format(args.output))
    with open(args.output, 'w') as outfile:
        generate.generate_slides(tags, filenames, outfile)

if __name__ == '__main__':
    main()
