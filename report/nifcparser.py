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
            'report': """<td\ height="629"\ colspan="3"><p\ class="tableHeading">(?P<date>[^<]+)</p>(?P<blob>.*)\.</p></td>""",
            'acres_active': """<td\ height="54">Acres\ from\ active\ fires\ </td>
[\s]+<td>(?P<acres>[^<]+)</td>""",
            'new_fires': """<td width="345">Number of new large fires </td>
.*<td width="105">4</td>"""
        }

    def compile_regex(self, pattern):
        """ Take one of the self.regexes and run it against the markup.
            Return a findall object.
            """
        regex = re.compile(self.regexes[pattern], re.MULTILINE|re.VERBOSE|re.IGNORECASE|re.DOTALL)
        r = regex.search(self.markup)
        regex.match(self.markup)
        return regex.findall(self.markup)

    def get_large_fire_list(self):
        """ Turn the large fire list into a dict.
            """
        pass

def main(args):
    p = NIFCparser()
    parts = p.compile_regex('report')
    parts = p.compile_regex('acres_active')
    print parts

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
