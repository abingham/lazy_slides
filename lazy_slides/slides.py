import argparse
import concurrent.futures as futures
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
    '''Parse the command line arguments.

    :return: The "namespace object" return by
      `argparse.ArgumentParser.parse_args()`.
    '''
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
    parser.add_argument(
        '-w, --workers',
        dest='num_workers',
        type=int,
        default=0,
        metavar='INT',
        help='The number of worker threads or processes to use.')

    return parser.parse_args()

def init_logging(verbose):
    '''Initialized the logging system.

    If `verbose` is `True`, the logging level will be
    `DEBUG`. Otherwise, it'll be `WARNING`.

    :param verbose: Whether logging should be verbose.
    :type verbose: bool
    '''
    if verbose:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    logging.basicConfig(
        level=level,
        stream=sys.stdout)

def init_search_function(search_function):
    '''Initialize the search function.

    This takes a function specified by its fully-qualified name. This
    imports the necessary module(s) and looks up the function in that
    module. Once it's found, this sets
    `lazy_slides.search.search_function` to that function.

    :param search_function: The fully-qualified name of a function to
      search for image matches.
    :type search_function: str
    '''

    from . import search

    toks = search_function.split('.')
    module_name = '.'.join(toks[:-1])
    func_name = toks[-1]

    mod = importlib.import_module(module_name)

    search.search_function = getattr(mod, func_name)

def process_tag(tag):
    '''Search, download, and convert a single image based on a single
    tag.

    :param tag: The tag to search on.
    :param throw_on_failure: Whether an exception should be thrown if
      when no match is found.

    :return: A tuple (tag, filename) defining the match. If there was
       no match, filename will be None.
    '''
    url = search.search_photos(tag)
    out_filename = None

    if url is not None:
        in_filename = download.download(url)
        out_filename = manipulation.convert(in_filename)

    return (tag, out_filename)

def main():
    args = parse_args()
    init_logging(args.verbose)
    init_search_function(args.search_function)

    # Determine how many workers we should use. If no number is
    # specified, make one per tag.
    num_workers = args.num_workers
    if num_workers == 0:
        num_workers = len(args.tags)
    log.info('Using {} workers'.format(num_workers))

    # Run the searches/downloads concurrently.
    executor = futures.ThreadPoolExecutor(num_workers)
    results = executor.map(
        process_tag,
        args.tags)

    def filter_failure(rslt):
        '''Filter out failed searches, throwing if we're configured to
        do so.
        '''
        if rslt[1] is None:
            if args.fail_on_missing:
                raise ValueError('No match for {}'.format(rslt[0]))
            return False
        else:
            return True

    # Filter out match failures
    results = filter(filter_failure, results)
    tags, filenames = zip(*results)

    # Generate the slideshow.
    log.info('Writing output to file {}'.format(args.output))
    with open(args.output, 'w') as outfile:
        generate.generate_slides(tags, filenames, outfile, args)

if __name__ == '__main__':
    main()
