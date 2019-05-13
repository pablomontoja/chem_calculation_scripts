#!/bin/bash
#
if [ ! -d "error" ]; then
  mkdir error
fi


for f in *.den
do
	mv "${f%%.*}".mop error/"${f%%.*}".mop
	mv "${f%%.*}".out error/"${f%%.*}".out
	mv "${f%%.*}".pbs error/"${f%%.*}".pbs
	mv "${f%%.*}".xyz error/"${f%%.*}".xyz
	mv "${f%%.*}".res error/"${f%%.*}".res
	mv "${f%%.*}".den error/"${f%%.*}".den
done