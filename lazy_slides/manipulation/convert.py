import logging
import os

from .PythonMagickWand import *


log = logging.getLogger(__name__)

def convert(infilename, target_type='png'):
    '''Convert an image from one type to another.

    This uses MagickWand to convert an input file into another
    type. After conversion, the original file is deleted.

    :param infilename: The name of the file to convert.
    :param target_type: The new image type to save as.
    '''

    outfilename = '{}.{}'.format(
        os.path.splitext(infilename)[0],
        target_type)

    log.info('Converting {} to {}.'.format(
            infilename,
            outfilename))

    wand = NewMagickWand()
    MagickReadImage(wand, infilename.encode('utf-8'))
    MagickWriteImage(wand, outfilename.encode('utf-8'))

    # TODO: Reconsider this. The deletion should probably occur
    # elsewhere (if anywhere.) Having it here will mess with caching,
    # etc.
    #
    # Delete original
    if infilename != outfilename:
        log.debug('Deleting {}'.format(infilename))
        os.remove(infilename)

    return outfilename
