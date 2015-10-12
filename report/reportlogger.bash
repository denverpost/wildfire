#!/bin/bash
# Logs when a new fire report is published on http://www.nifc.gov/fireInfo/nfn.htm, then sends it to a parser
# Example:
# $ ./reportlogger.bash

# Environment variables are stored in project root.
# Currently two variables are set in it:
#   $RECIPIENTS, a space-separated list of email addresses to send to
#   $SENDER, the sending email address.
source ../.source.bash

# Default arguments
URL='http://www.nifc.gov/fireInfo/nfn.htm'
TEST=0
SLUG='report.html'

# What arguments do we pass?
while [ "$1" != "" ]; do
	case $1 in
		-u | --url ) shift
			URL=$1
			;;
		-t | --test ) shift
			TEST=1
			;;
	esac
	shift
done

# DOWNLOAD!
# If we're not testing, we download the file
if [ "$TEST" -eq 0 ]; then wget -q -O "$SLUG.new" $URL; fi


# We make sure the files exist
if [ ! -f "$SLUG.old" ]; then touch "$SLUG.old"; fi
if [ ! -f "$SLUG.current" ]; then touch "$SLUG.current"; fi
touch "$SLUG.new"

# If the file's empty or near-empty, exit
FILESIZE=$(du -b "$SLUG.new" | cut -f 1)
if [ $FILESIZE -lt 200 ]; then
    exit 2;
fi

# COMPARE!
# If there are any differences, we store the new version and log the diff.
# We also run the parser.
DIFF=`diff "$SLUG.current" "$SLUG.new"`
if [ -n "$DIFF" ]
then
    echo "DIFF in $SLUG.$STATE"
	DATE=`date +'%F-%H-%M'`
    if [ ! -d "$SLUG" ]
    then
	    mkdir $SLUG
    fi
	rm "$SLUG.old"
	mv "$SLUG.current" "$SLUG.old"
	mv "$SLUG.new" "$SLUG.current"
	cp "$SLUG.current" "$SLUG/the.file.$DATE"
	echo $DIFF > "$SLUG/the.diff.$DATE"

    # Build a CSV of the fire data.
    ###python geomacparser.py --state $STATE

    # Store a diff of the CSV that we email to our people.
    ###diff "$STATE-fires.csv" "$STATE-fires-new.csv" > "$STATE-fires-diff.csv"
    # The $SENDER and $RECIPIENTS are set via environment variables.
    ###python mailer.py --state $STATE --sender $SENDER $RECIPIENTS
    ###rm "$STATE-fires.csv"; mv "$STATE-fires-new.csv" "$STATE-fires.csv"
    
else
	echo "NO DIFF in $SLUG"
	rm "$SLUG.new"
	exit 2
fi

echo "DONE"
exit 1
