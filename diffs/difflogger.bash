#!/bin/bash
# Logs changes to a file if there are any.
# Example use (for extracting a chunk of text from another file):
# $ ./difflogger.bash --url http://www.berkshireeagle.com/


# Default arguments
URL='http://rmgsc.cr.usgs.gov/outgoing/GeoMAC/current_year_fire_data/KMLS/'
TEST=0
SLUG='kml_list'

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


# EXTRACT TEXT!
# Note: OS X sed is different. We need gnu-sed on OS X. 
# Run $ brew install gnu-sed
# and get yourself gsed.
# 
# We run both gsed and sed because nothing really matters...
# at least when it comes to this.
gsed -ni "/Parent Directory/,/<hr>/p" "$SLUG.new"
sed -i "/Parent Directory/,/<hr>/p" "$SLUG.new"


# We make sure the files exist
if [ ! -f "$SLUG.old" ]; then touch "$SLUG.old"; fi
if [ ! -f "$SLUG.current" ]; then touch "$SLUG.current"; fi
touch "$SLUG.new"

# COMPARE!
# If there are any differences, we store the new version and log the diff.
DIFF=`diff "$SLUG.current" "$SLUG.new"`
if [ -n "$DIFF" ]
then
    echo "DIFF in $SLUG"
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
else
	echo "NO DIFF in $SLUG"
	rm "$SLUG.new"
	exit 2
fi

echo "DONE"
exit 1
