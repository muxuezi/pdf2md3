#!/miniconda3/bin/python

import sys
import os
from parser import Parser
from writer import Writer
from syntax import UrbanSyntax


def main(argv):
    if len(argv) == 2:
        filename = argv[1]
        title = os.path.splitext(os.path.basename(filename))[0]
        print('Parsing', filename)
    else:
        print('usage:')
        print('    python main.py <pdf>')
        return

    parser = Parser(filename)
    parser.extract()
    piles = parser.parse()

    syntax = UrbanSyntax()

    writer = Writer()
    writer.set_syntax(syntax)
    writer.set_mode('simple')
    writer.set_title(title)
    writer.write(piles)

    print('Your markdown is at', writer.get_location())


if __name__ == '__main__':
    main(sys.argv)
