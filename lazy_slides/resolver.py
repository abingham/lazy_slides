import logging
import os.path

from . import download
from . import manipulation
from . import search

log = logging.getLogger(__name__)

class Resolver:
    def __init__(self,
                 tag,
                 config,
                 fname,
                 base_fname):
        self.config = config
        self.tag = tag
        self.fname = fname
        self.base_fname = base_fname

        self.success = False

    def _download(self, urls):
        for url in urls:
            try:
                filename = download.download(
                    url,
                    self.config.directory)

                return filename
            except Exception:
                log.exception('Error processing url {}'.format(url))

        raise IOError(
            'Unable to download image for tag {}'.format(
                self.tag))

    def _resolve_base(self):
        if self.base_fname:
            return

        urls = search.search(self.tag, count=5)
        filename = self._download(urls)
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

        self.success = True
        return (self.tag, self.fname)
