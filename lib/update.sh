#!/bin/bash

# Stop on errors.
set -u

DJANGO_DIR=Django-1.7.1
WAITRESS_DIR=waitress-0.8.9
MARKDOWN_DIR=Markdown-2.5.2
PLY_DIR=ply-3.4

echo "*** Updating django from $DJANGO_DIR"
cd $DJANGO_DIR
zip -ur ../packages.zip django/*
cd ..
echo "*** Done."

echo "*** Updating waitress from $WAITRESS_DIR"
cd $WAITRESS_DIR
zip -ur ../packages.zip waitress/*
cd ..
echo "*** Done."

echo "*** Updating markdown from $MARKDOWN_DIR"
cd $MARKDOWN_DIR
zip -ur ../packages.zip markdown/*
cd ..
echo "*** Done."

echo "*** Updating ply from $PLY_DIR"
cd $PLY_DIR
zip -ur ../packages.zip ply/*
cd ..
echo "*** Done."

echo "*** Adding argparse.py"
zip -ur packages.zip argparse.py
echo "*** Done."