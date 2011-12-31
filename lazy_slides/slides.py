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
    parser.add_argument(
        '-W, --image-width',
        dest='image_width',
        type=int,
        default=200,
        metavar='INT',
        help='The width of the slide image.')
    parser.add_argument(
        '-H, --image-height',
        dest='image_height',
        type=int,
        default=200,
        metavar='INT',
        help='The height of the slide image.')

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

def zip_filter(func, seq, *seqs):
    for tup in zip(seq, *seqs):
        if func(tup[0]):
            yield tup

def main():
    args = parse_args()
    init_logging(args.verbose)
    init_search_function(args.search_function)

    def filter_failures(url_tag):
        url = url_tag[0]
        tag = url_tag[1]

        if url is None:
            if args.fail_on_missing:
                raise ValueError(
                    'No matching images for tag "{}"'.format(
                        tag))
            return False

        else:
            return True

    urls = map(
        search.search_photos,
        args.tags)

    url_tags = filter(
        filter_failures,
        zip(urls, args.tags))

    urls, tags = zip(*url_tags)

    in_filenames = map(
        download.download,
        urls)

    out_filenames = map(
        manipulation.convert,
        in_filenames)

    out_filenames = map(
        lambda fname: manipulation.resize(
            fname,
            fname,
            (args.image_width,
             args.image_height)),
        out_filenames)

    log.info('Writing output to file {}'.format(args.output))

    with open(args.output, 'w') as outfile:
        generate.generate_slides(tags, out_filenames, outfile)

if __name__ == '__main__':
    main()
