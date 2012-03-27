import argparse
import futures
import importlib
import logging
import os
import sys

from .cache import open_cache
from .cpu_count import cpu_count
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
    parser.add_argument(
        '-d, --directory',
        dest='directory',
        default='.lazy_slides',
        metavar='DIRECTORY',
        help='The directory used to hold lazy-slides data.')

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

class Builder:
    def __init__(self, args):
        self.args = args
        self.directory = self.args.directory

    def fetch_base(self,
                   search_function,
                   tag,
                   cache):
        fname = cache.get(search_function, tag)
        if fname is not None:
            return fname

        url = search.search(tag)
        filename = download.download(url, self.directory)
        filename = manipulation.convert(filename)

        # TODO: Delete original downloaded file if it's different than
        # the converted version.

        cache.set(search_function, tag, None, None, filename)
        return filename

    def fetch(self,
              search_function,
              tag,
              width,
              height,
              cache):
        '''Search, download, and convert a single image based on a
        single tag.
        '''

        # See if we've got the resized image already
        fname = cache.get(search_function, tag, width, height)
        if fname is not None:
            return (tag, fname)

        base_fname = self.fetch_base(search_function, tag, cache)
        (fname, ext) = os.path.splitext(base_fname)

        fname = '{}.{}.{}{}'.format(
            fname, width, height, ext)

        manipulation.resize(base_fname, fname, (width, height))

        cache.set(search_function, tag, width, height, fname)

        return (tag, fname)

    def run(self, cache):
        # Determine how many workers we should use. If no number is
        # specified, make one per tag.
        num_workers = self.args.num_workers
        if num_workers < 1:
            try:
                num_workers = cpu_count()
            except NotImplementedError:

                log.info('num_cpus() not implemented. Using default worker count.')
                num_workers = 4

        log.info('Using {} workers'.format(num_workers))

        with futures.ThreadPoolExecutor(num_workers) as e:
            func = lambda tag: self.fetch(self.args.search_function,
                                          tag,
                                          self.args.image_width,
                                          self.args.image_height,
                                          cache)

            tag_map = dict(
                e.map(func, set(self.args.tags)))

        # Generate the slideshow.
        log.info('Writing output to file {}'.format(self.args.output))
        with open(self.args.output, 'w') as outfile:
            generate.generate_slides(
                self.args.tags,
                tag_map,
                outfile,
                self.args)

def main():
    args = parse_args()
    init_logging(args.verbose)
    init_search_function(args.search_function)

    bld = Builder(args)

    try:
        if not os.path.exists(args.directory):
            log.info('Creating data directory: {}'.format(args.directory))
            os.makedirs(args.directory)

        cache_file = os.path.join(args.directory, 'cache.db')
        with open_cache(cache_file, 100) as cache:
            bld.run(cache)
    except Exception:
        log.exception('Exception while building slides:')

if __name__ == '__main__':
    main()
