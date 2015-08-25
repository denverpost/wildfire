#!/usr/bin/env python
# Structure all the data.
import os, sys, doctest, csv
import argparse
import re
from datetime import datetime

class NIFCparser:
    """ There are at least three separate types of data we're extracting,
        so this class makes it as easy as we can make it to do that.
        """

    def __init__(self):
        self.filename = 'report.html.current'

        fh = open(self.filename, 'r')
        self.markup = fh.read()
        fh.close
        
        self.regexes = {
            'report': """<td\ height="629"\ colspan="3"><p\ class="tableHeading">(?P<date>[^<]+)</p>(?P<blob>.*)\.</p></td>"""
        }

    def get_blob(self):
        """ Get a blob of text, such as the report or the weather.
            """
        regex = re.compile(self.regexes['report'], re.MULTILINE|re.VERBOSE|re.IGNORECASE|re.DOTALL)
        r = regex.search(self.markup)
        regex.match(self.markup)
        parts = regex.findall(self.markup)
        print parts

    def get_stats(self):
        """ Get the individual stats, such as # of new large fires or
            active fire acres.
            """
        pass

    def get_large_fire_list(self):
        """ Turn the large fire list into a dict.
            """
        pass

def main(args):
    p = NIFCparser()
    p.get_blob()

def build_parser(args):
    """ A method to make arg parsing testable.
        """
    parser = argparse.ArgumentParser(usage='', description='Handle the options.',
                                     epilog='')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    return parser.parse_args()

if __name__ == '__main__':
    args = build_parser(sys.argv)

    if args.verbose:
        doctest.testmod(verbose=args.verbose)

    main(args)
