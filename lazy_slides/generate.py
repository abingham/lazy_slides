def generate_slides(tags, filenames, outfile):
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
