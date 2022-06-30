#!/bin/bash

# Run the R script generating images
Rscript analysis.R

# Make the images directory if it does not exist
mkdir -p figures

# Move all images to images directory
mv *.png figures
