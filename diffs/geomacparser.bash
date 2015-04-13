#!/bin/bash
# Parse GEOMAC's list of KML files and return HTML or a CSV.
# Takes a filename as input and goes line-by-line through the file.
# Usage:
# $ ./geomacparser.bash kml_list.CO.current
#
# Example line from an input file:
# <a href="CO-MFX-JK2S%20Strawberry%203-31-2015%201530.kml">CO-MFX-JK2S Strawberry 3-31-2015 1530.kml</a>            2015-04-03 13:33  3.7K

$FILE = ''

# Turn arguments into something we can use
while [ "$1" != "" ]; do
    case $1 in
        -f | --file ) shift
            FILE=$1
            ;;
        -t | --test ) shift
            TEST=1
            ;;
    esac
    shift
done

if [ ! -f "$FILE" ]; then
    echo "Couldn't find file $FILE, please pass a --file FILENAME argument to this script."
    exit 2
fi

cat $FILE
