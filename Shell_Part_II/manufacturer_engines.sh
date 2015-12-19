#!/bin/bash

FILENAME=$1
MANUFACTURER=$2

csvgrep -d '^' -c manufacturer -m Airbus $FILENAME $MANUFACTURER |csvsort -r -c nb_engines|csvcut -c model|head -n 2|tail -n +2
