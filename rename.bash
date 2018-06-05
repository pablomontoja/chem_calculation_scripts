#!/bin/sh
for file in *.gjf; do
  if [ -e "$file" ]; then
    newname=`echo "$file" | sed 's/_FREQ//'`
    #echo $newname
    mv "$file" "$newname"
  fi
done
