#!/bin/bash
# Logs changes to GEOMAC's list of fire perimeters at http://rmgsc.cr.usgs.gov/outgoing/GeoMAC/current_year_fire_data/KMLS/
# Example:
# $ ./difflogger.bash --state CO


# Default arguments
URL='http://rmgsc.cr.usgs.gov/outgoing/GeoMAC/current_year_fire_data/KMLS/'
TEST=0
SLUG='kml_list'
STATE='all'

# What arguments do we pass?
while [ "$1" != "" ]; do
	case $1 in
		-u | --url ) shift
			URL=$1
			;;
		-t | --test ) shift
			TEST=1
			;;
        -s | --state ) shift
            STATE=$1
            ;;
	esac
	shift
done

# DOWNLOAD!
# If we're not testing, we download the file
if [ "$TEST" -eq 0 ]; then wget -q -O "$SLUG.$STATE.new" $URL; fi


# EXTRACT TEXT!
# Note: OS X sed is different. We need gnu-sed on OS X. 
# Run $ brew install gnu-sed
# and get yourself gsed.

# We run both gsed and sed because nothing really matters...
# at least when it comes to this.
gsed -ni "/Parent Directory/,/<hr>/p" "$SLUG.$STATE.new"
sed -i "/Parent Directory/,/<hr>/p" "$SLUG.$STATE.new"


# We make sure the files exist
if [ ! -f "$SLUG.$STATE.old" ]; then touch "$SLUG.$STATE.old"; fi
if [ ! -f "$SLUG.$STATE.current" ]; then touch "$SLUG.$STATE.current"; fi
touch "$SLUG.$STATE.new"

# If we want to filter by state, do it.
if [ "$STATE" != 'all' ]; then
    grep "$STATE-" "$SLUG.$STATE.new" > tmp; mv tmp "$SLUG.$STATE.new"
fi

# COMPARE!
# If there are any differences, we store the new version and log the diff.
# We also run the parser.
DIFF=`diff "$SLUG.$STATE.current" "$SLUG.$STATE.new"`
if [ -n "$DIFF" ]
then
    echo "DIFF in $SLUG.$STATE"
	DATE=`date +'%F-%H-%M'`
    if [ ! -d "$SLUG-$STATE" ]
    then
	    mkdir $SLUG-$STATE
    fi
	rm "$SLUG.$STATE.old"
	mv "$SLUG.$STATE.current" "$SLUG.$STATE.old"
	mv "$SLUG.$STATE.new" "$SLUG.$STATE.current"
	cp "$SLUG.$STATE.current" "$SLUG-$STATE/the.file.$DATE"
	echo $DIFF > "$SLUG-$STATE/the.diff.$DATE"

    python geomacparser.py --state $STATE
    python mailer.py --state $STATE jmurphy@denverpost.com khamm@denverpost.com
    
else
	echo "NO DIFF in $SLUG"
	rm "$SLUG.$STATE.new"
	exit 2
fi

echo "DONE"
exit 1
