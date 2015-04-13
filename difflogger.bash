#!/bin/bash
# Logs changes to a file if there are any.
# Example use (for extracting a chunk of text from another file):
# $ ./difflogger.bash -u http://www.berkshireeagle.com/ --slug FFglobalheader --fragment


# Default arguments
URL='http://extras.mnginteractive.com/live/css/site67/bartertown.css'
TEST=0
FRAGMENT=0
DOMAINS=0

# What arguments do we pass?
while [ "$1" != "" ]; do
	case $1 in
		-u | --url ) shift
			URL=$1
			;;
		-s | --slug ) shift
			SLUG=$1
			;;
		-d | --domains ) shift
			DOMAINS=1
			;;
		-f | --fragment ) shift
			FRAGMENT=1
			;;
		-t | --test ) shift
			TEST=1
			;;
	esac
	shift
done

# If we don't have a slug passed, see if we can pull one out of the URL.
if [ -z "$SLUG" ]
then
	# To see why this works: http://stackoverflow.com/questions/3162385/how-to-split-a-string-in-shell-and-get-the-last-field
	SLUG=${URL##*/}
	if [ -z "$SLUG" ]; then exit 2; fi
fi

# DOMAIN-SPECIFIC HANDLING
if [ "$DOMAINS" -eq 1 ]; then
    for DOMAIN in `cat domains`; do
        URL="http://local.$DOMAIN.com/assets/header-footer.json"
        SLUG=$DOMAIN
        DIR="header-footer.json/"
        if [ "$TEST" -eq 0 ]; then wget -q -O "$DIR$SLUG.new" $URL; fi
        if [ $(stat -c%s "$DIR$SLUG.new") -lt 200 ]; then echo "$SLUG TOO SMALL ( $(stat -c%s "$DIR$SLUG.new") )"; continue; fi
        if [ ! -f "$DIR$SLUG.old" ]; then touch "$DIR$SLUG.old"; fi
        if [ ! -f "$DIR$SLUG.current" ]; then touch "$DIR$SLUG.current"; fi
        touch "$SLUG.new"
        DIFF=`diff "$DIR$SLUG.current" "$DIR$SLUG.new"`
        if [ -n "$DIFF" ]
        then
        	echo "DIFF in $SLUG"
        	DATE=`date +'%F-%H-%M'`
        	mkdir $DIR$SLUG
        	rm "$DIR$SLUG.old"
        	mv "$DIR$SLUG.current" "$DIR$SLUG.old"
        	mv "$DIR$SLUG.new" "$DIR$SLUG.current"
        	cp "$DIR$SLUG.current" "$DIR$SLUG/the.file.$DATE"
        	echo $DIFF > "$DIR$SLUG/the.diff.$DATE"
        else
        	echo "NO DIFF in $SLUG"
        	rm "$SLUG.new"
        fi
    done
    exit 1
fi

# DOWNLOAD!
# If we're not testing, we download the file
if [ "$TEST" -eq 0 ]; then wget -q -O "$SLUG.new" $URL; fi


# EXTRACT TEXT!
if [ "$FRAGMENT" -eq 1 ]; then sed -i "/###START-$SLUG/,/###END-$SLUG/ !d" "$SLUG.new"; fi


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
	mkdir $SLUG
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
