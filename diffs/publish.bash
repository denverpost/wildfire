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


../ftp.bash --dir $REMOTE_DIR --source_dir output --host $REMOTE_HOST
