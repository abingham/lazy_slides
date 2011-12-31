import logging

from .PythonMagickWand import *


log = logging.getLogger(__name__)

def resize(infilename,
           outfilename,
           new_size):
    '''Resize an image file.

    :param infilename: The input image file name.
    :param outfilename: The output image file name.
    :param new_size: A tuple (width, height) of the new image size.
    '''

    log.info('Resizing {} to {}. New size = {}'.format(
            infilename,
            outfilename,
            new_size))

    wand = NewMagickWand()
    MagickReadImage(wand, infilename.encode('utf-8'))
    MagickScaleImage(wand, new_size[0], new_size[1])
    MagickWriteImage(wand, outfilename.encode('utf-8'))

    return outfilename
