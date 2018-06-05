#!/bin/bash
for f in *.log
do
	babel -ig09 $f -oxyz "${f%%.*}".xyz
	tail -n +3 "${f%%.*}".xyz > "${f%%.*}".gjf
	echo "" >> "${f%%.*}".gjf
done


