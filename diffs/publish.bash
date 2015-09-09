#!/bin/bash
# Publish the CSVs as JSON.
# Currently we're publishing a list of the recent fires.

STATE='all'

# What arguments do we pass?
while [ "$1" != "" ]; do
	case $1 in
		-t | --test ) shift
			TEST=1
			;;
        -s | --state ) shift
            STATE=$1
            ;;
	esac
	shift
done

if [ ! -d "output" ]
then
    mkdir output
fi

csvsql --query "select * from '$STATE-fires' GROUP BY fire ORDER BY datetime DESC" $STATE-fires.csv | csvjson > output/$STATE-fires.json

# Download the KML to our server, if we haven't downloaded it already.
for ITEM in `csvsql --query "select state, url from '$STATE-fires' ORDER BY datetime DESC" $STATE-fires.csv`;
do
    STATE=`echo $ITEM | cut -d',' -f1`
    URL=`echo $ITEM | cut -d',' -f2`

    # This regex captures everything after the final "/" in the url.
    FILENAME=`expr "$URL" : '.*\/\(.*\)'`
    FILENAME=${FILENAME//%20/_}

    if [ ! -d "output/$STATE" ];
    then
        mkdir output/$STATE
    fi

    if [ ! -e "output/$STATE/$FILENAME" ];
    then
        wget -O "output/$STATE/$FILENAME" "$URL"
        echo $FILENAME
    fi
done

../ftp.bash --dir $REMOTE_DIR --source_dir output --host $REMOTE_HOST
