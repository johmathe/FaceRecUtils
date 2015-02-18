#!/bin/bash
ORIGINALS=/home/johmathe/dataset/artists
TRIMMED=/home/johmathe/dataset/trimmed
DETECT=/home/johmathe/ccv/bin/scddetect
FACEMODEL=/home/johmathe/ccv/samples/face.sqlite3

for d in $ORIGINALS/*; do
  ARTIST_DIR=$TRIMMED/$(basename $d)
  mkdir -p $ARTIST_DIR
  for f in $d/*; do
    $DETECT $f $FACEMODEL | python trimfaces.py $f $ARTIST_DIR/$(basename $f) & 
  done
done
