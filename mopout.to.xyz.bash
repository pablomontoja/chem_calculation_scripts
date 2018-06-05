#!/bin/bash
for f in *.out
do
	babel -imopout $f -oxyz "${f%%.*}_result".xyz
	# tail -n +3 $f > "${f%%.*}".gjf
	# echo "" >> "${f%%.*}".gjf
done

