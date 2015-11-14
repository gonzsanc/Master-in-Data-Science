#!/bin/sh
# $1 - name of the csv file
# $2 -number of engines

csvgrep -d '^' -c nb_engines -m$2 $1|csvcut -c manufacturer|sort|uniq|wc -l
