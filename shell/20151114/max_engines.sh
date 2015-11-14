#!/bin/sh

echo 'The highest number of engines corresponds to: '
csvsort -d'^' -c nb_engines -r  optd_aircraft.csv|head -2|csvcut -c manufacturer|tail -n +2