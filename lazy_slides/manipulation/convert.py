import logging
import os

from .PythonMagickWand import *


log = logging.getLogger(__name__)

def convert(infilename, target_type='png'):
    outfilename = '{}.{}'.format(
        os.path.splitext(infilename)[0],
        target_type)

    log.info('Converting {} to {}.'.format(
            infilename,
            outfilename))

    wand = NewMagickWand()
    MagickReadImage(wand, infilename.encode('utf-8'))
    MagickWriteImage(wand, outfilename.encode('utf-8'))

    # Delete original
    log.debug('Deleting {}'.format(infilename))
    os.remove(infilename)

    return outfilename
