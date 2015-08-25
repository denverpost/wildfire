#!/usr/bin/env python
# Structure all the data.
import os, sys, doctest, csv
import argparse
import re
from datetime import datetime

def main(args):
    pass

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
