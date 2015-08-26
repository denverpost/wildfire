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
            'report': """<td\ height="629"\ colspan="3"><p\ class="tableHeading">(?P<date>[^<]+)</p>(?P<report>.*)\.</p></td>""",
            'fires_active': """\s+Total\ does\ not\ include\ individual\ fires\ within\ complexes.</em></span></td>
\s+<td>(?P<fires_active>[0-9]+)</td>""",
            'acres_active': """<td\ height="54">Acres\ from\ active\ fires\ </td>
\s+<td>(?P<acres_active>[^<]+)</td>""",
            'new_fires': """<td\ width="345">Number\ of\ new\ large\ fires\ </td>
\s+<td\ width="105">(?P<new_fires>[0-9]+)</td>""",
            'fires_active_by_state': """<td\ rowspan="3"><p>(?P<fires_active_by_state>.*)</p></td>
\s+</tr>
\s+<tr>""",
            'fires_active_item': """\s?(?P<state>[A-Za-z ]+ )\ \((?P<fires>[0-9]+)\)\s?(<br\ />)?"""
        }

    def compile_regex(self, pattern):
        """ Take one of the self.regexes and run it against the markup.
            Return a dict object.
            """
        regex = re.compile(self.regexes[pattern], re.MULTILINE|re.VERBOSE|re.IGNORECASE|re.DOTALL)
        r = regex.search(self.markup)
        return r.groupdict()

    def get_fires_active_by_state(self):
        """ Turn the large fire list into a dict.
            """
        raw = self.compile_regex('fires_active_by_state')
        regex = re.compile(self.regexes['fires_active_item'], re.MULTILINE|re.VERBOSE|re.IGNORECASE|re.DOTALL)
        regex.match(raw['fires_active_by_state'])
        return regex.findall(self.markup)
        

def main(args):
    p = NIFCparser()
    parts = p.compile_regex('report')
    parts = p.compile_regex('acres_active')
    parts = p.compile_regex('fires_active')
    parts = p.compile_regex('fires_active_by_state')
    print parts
    fire_list = p.get_fires_active_by_state()
    print fire_list

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
