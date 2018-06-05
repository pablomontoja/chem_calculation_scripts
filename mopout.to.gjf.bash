#!/bin/bash
for f in *.out
do
	babel -imopout $f -oxyz "${f%%.*}".xyz
	tail -n +3 "${f%%.*}".xyz > "${f%%.*}".gjf
	echo "" >> "${f%%.*}".gjf
done

