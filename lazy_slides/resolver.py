import os.path

from . import download
from . import manipulation
from . import search

class Resolver:
    def __init__(self,
                 tag,
                 config,
                 cache):
        self.config = config
        self.tag = tag

        self.fname = cache.get(
            self.config.search_function,
            tag,
            self.config.image_width,
            self.config.image_height)

        self.base_fname = None

        if self.fname is None:
            self.base_fname = cache.get(
                self.config.search_function,
                tag)

    def _resolve_base(self):
        if self.base_fname:
            return

        url = search.search(self.tag)
        filename = download.download(
            url,
            self.config.directory)

        self.base_fname = manipulation.convert(filename)

        # TODO: Delete original downloaded file if it's different than
        # the converted version.

    def resolve(self):
        if self.fname is None:
            self._resolve_base()
            assert self.base_fname is not None

            (fname, ext) = os.path.splitext(self.base_fname)

            self.fname = '{}.{}.{}{}'.format(
                fname,
                self.config.image_width,
                self.config.image_height,
                ext)

            manipulation.resize(self.base_fname,
                                self.fname,
                                (self.config.image_width,
                                 self.config.image_height))

        assert self.fname is not None
        return (self.tag, self.fname)

    def update_cache(self, cache):
        if self.fname is not None:
            cache.set(self.config.search_function,
                      self.tag,
                      self.config.image_width,
                      self.config.image_height,
                      self.fname)

        if self.base_fname is not None:
            cache.set(self.config.search_function,
                      self.tag,
                      None,
                      None,
                      self.base_fname)