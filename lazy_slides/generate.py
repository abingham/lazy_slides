def generate_slides(tags,
                    tag_map,
                    outfile,
                    args):
    '''Generate a beamer slideshow.

    :param tags: The tags used to find the images in the slideshow.
    :param filenames: The filenames of the images for the slideshow.
    :param outfile: The name of the file into which the results should
      be saved.
    '''
    outfile.write('\\documentclass{beamer}\n')
    outfile.write('\\usetheme{Copenhagen}\n')
    outfile.write('\\begin{document}\n')
    for tag in tags:
        outfile.write('\\begin{frame}\n')
        outfile.write('\\frametitle{{{}}}'.format(tag))
        outfile.write('\\begin{center}\n')
        outfile.write('\\includegraphics[width={width}px, height={height}px]{{{filename}}}'.format(
                width=args.image_width,
                height=args.image_height,
                filename=tag_map[tag]))
        outfile.write('\\end{center}\n')
        outfile.write('\\end{frame}\n')
    outfile.write('\\end{document}\n')
