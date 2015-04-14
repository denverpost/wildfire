#!/usr/bin/env python
# Parse GEOMAC's list of KML files and return HTML or a CSV.
import os, sys, doctest, csv, argparse
import re
from datetime import datetime
#from bs4 import BeautifulSoup

# Takes a filename as input and goes line-by-line through the file.
# Usage:
# $ ./geomacparser.py kml_list.CO.current
#
# Example line from an input file:
# <a href="CO-MFX-JK2S%20Strawberry%203-31-2015%201530.kml">CO-MFX-JK2S Strawberry 3-31-2015 1530.kml</a>            2015-04-03 13:33  3.7K

#    echo "Couldn't find file $FILE, please pass a --file FILENAME argument to this script."

def main(args):
    fn = 'kml_list.%s.current' % args.state
    fh = open(fn, 'rb')
    content = []
    url_prefix = 'http://rmgsc.cr.usgs.gov/outgoing/GeoMAC/current_year_fire_data/KMLS/'

    for line in fh.readlines():
        if 'Last modified' in line:
            continue
        line = line.strip()
        #print line
        pattern = '.*href="(?P<href>[^"]+)">(?P<slug>[^ ]+)\ (?P<fire>[^0-9]+)(?P<date>[0-9]{1,2}-[0-9]{1,2}-[0-9]{4})\ (?P<time>[0-9]{4})'
        regex = re.compile(pattern, re.VERBOSE|re.IGNORECASE|re.DOTALL)
        r = regex.search(line.strip())
        regex.match(line.strip())
        parts = regex.findall(line)
        #print parts
        if parts == []:
            print line

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='', description='Handle the options we handle.',
                                     epilog='')
    parser.add_argument('-s', '--state', dest='state', action='store',
                        default='all',
                        help='a two-letter abbreviation for the state we want to process, i.e. CO CA AZ etc.')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    args = parser.parse_args()
    print dir(args)
    print args.state

    if args.verbose:
        doctest.testmod(verbose=args.verbose)

    main(args)
