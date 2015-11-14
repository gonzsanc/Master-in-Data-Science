#!/bin/sh

echo el primer argumento es $1
echo el segundo argumento es $2
echo el número de argumentos es $#

echo 'The highest number of engines corresponds to: '
csvsort -d'^' -c nb_engines -r  $1|head -2|csvcut -c manufacturer|tail -n +2