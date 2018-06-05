#!/bin/bash
for f in *.xyz
do
	tail -n +3 $f > "${f%%.*}".gjf
	echo "" >> "${f%%.*}".gjf
done