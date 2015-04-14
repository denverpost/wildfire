#!/usr/bin/env python
# Parse GEOMAC's list of KML files and return HTML or a CSV.
import os, sys, doctest, csv, argparse

# Takes a filename as input and goes line-by-line through the file.
# Usage:
# $ ./geomacparser.py kml_list.CO.current
#
# Example line from an input file:
# <a href="CO-MFX-JK2S%20Strawberry%203-31-2015%201530.kml">CO-MFX-JK2S Strawberry 3-31-2015 1530.kml</a>            2015-04-03 13:33  3.7K

#    echo "Couldn't find file $FILE, please pass a --file FILENAME argument to this script."

def main(args):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='', description='Handle the options we handle.',
                                     epilog='')
    parser.add_argument('-s', '--state', dest='state', action='store',
                        default='all',
                        help='a two-letter abbreviation for the state we want to process, i.e. CO CA AZ etc.')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    args = parser.parse_args()

    if args.verbose:
        doctest.testmod(verbose=args.verbose)

    main(args)
