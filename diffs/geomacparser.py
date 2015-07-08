#!/usr/bin/env python
# Parse GEOMAC's list of KML files and return HTML or a CSV.
import os, sys, doctest, csv
import argparse
import re
from datetime import datetime

# Takes a filename as input and goes line-by-line through the file.
# Usage:
# $ ./geomacparser.py kml_list.CO.current
#
# Example line from an input file:

#    echo "Couldn't find file $FILE, please pass a --file FILENAME argument to this script."

def main(args):
    fn = 'kml_list.%s.current' % args.state
    fh = open(fn, 'rb')
    content = [('state', 'fire', 'slug', 'datetime', 'url')]
    url_prefix = 'http://rmgsc.cr.usgs.gov/outgoing/GeoMAC/current_year_fire_data/KMLS/'

    for line in fh.readlines():
        """ We're matching lines such as:
<a href="CO-MFX-JK2S%20Strawberry%203-31-2015%201530.kml">CO-MFX-JK2S Strawberry 3-31-2015 1530.kml</a>            2015-04-03 13:33  3.7K
            And
<a href="FL-EVP-JGS7%20FFS%20152%20212%202-26-2015%200000.kml">FL-EVP-JGS7 FFS 152 212 2-26-2015 0000.kml</a>           2015-03-20 13:25  5.0K
        """
        if 'Last modified' in line:
            continue
        line = line.strip()
        pattern = '.*href="\
(?P<href>[^"]+)">(?P<slug>[^ ]+)\ \
(?P<fire>[^-]+) \
(?P<date>[0-9]{1,2}-[0-9]{1,2}-[0-9]{4})\ \
(?P<time>[0-9]{4})'
        regex = re.compile(pattern, re.MULTILINE|re.VERBOSE|re.IGNORECASE|re.DOTALL)
        r = regex.search(line.strip())
        regex.match(line.strip())
        parts = regex.findall(line)
        if parts == []:
            continue

        # Reorder the parts, do some data munging
        fire = parts[0][2].strip()
        slug = parts[0][1].strip()
        state = slug[:2]
        url = '%s%s' % (url_prefix, parts[0][0].strip())
        datetime = '%s %s' % (parts[0][3].strip(), parts[0][4].strip())
        content += [(state, fire, slug, datetime, url)]

    with open('%s-fires.csv' % args.state, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(content)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='', description='Handle the options.',
                                     epilog='')
    parser.add_argument('-s', '--state', dest='state', action='store',
                        default='all',
                        help='a two-letter abbreviation for the state we want to process, i.e. CO CA AZ etc.')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    args = parser.parse_args()

    if args.verbose:
        doctest.testmod(verbose=args.verbose)

    main(args)
