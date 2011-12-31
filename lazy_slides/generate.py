def generate_slides(tags, filenames, outfile):
    '''Generate a beamer slideshow.

    :param tags: The tags used to find the images in the slideshow.
    :param filenames: The filenames of the images for the slideshow.
    :param outfile: The name of the file into which the results should
      be saved.
    '''
    outfile.write('\\documentclass{beamer}\n')
    outfile.write('\\usetheme{Copenhagen}\n')
    outfile.write('\\begin{document}\n')
    for tag, filename in zip(tags, filenames):
        outfile.write('\\begin{frame}\n')
        outfile.write('\\frametitle{{{}}}'.format(tag))
        outfile.write('\\begin{center}\n')
        outfile.write('\\includegraphics[]{{{}}}'.format(filename))
        outfile.write('\\end{center}\n')
        outfile.write('\\end{frame}\n')
    outfile.write('\\end{document}\n')
