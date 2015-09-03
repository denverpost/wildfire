#!/usr/bin/env python
# Get the fire details included in the fire KML
import os, sys, doctest, csv
import argparse
import re
import geomacparser
from datetime import datetime

def main(args):
    pass

def build_parser(args):
    """ A method to make arg parsing testable.
        """
    parser = argparse.ArgumentParser(usage='', description='Handle the options.',
                                     epilog='')
    parser.add_argument('-s', '--state', dest='state', action='store',
                        default='all',
                        help='a two-letter abbreviation for the state we want to process, i.e. CO CA AZ etc.')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    return parser.parse_args()
    
# csvsql --query "SELECT fire, datetime, url FROM 'CO-fires' GROUP BY fire ORDER BY datetime DESC" CO-fires.csv

if __name__ == '__main__':
    args = build_parser(sys.argv)

    if args.verbose:
        doctest.testmod(verbose=args.verbose)

    main(args)
