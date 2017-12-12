#!/usr/bin/env bash

###
#  Find samfile with specific QNAME
#  Input: 
#    1) input SAM file; 
#    2) a text list of QNAME; 
#    3) output SAM file
#  Output:
#    print to screen the subset SAM file
#  Essentially a text grep in loop
###

# print file name input list 
inputAln=$1
inputId=$2

# detect if sam or bam file
if [ "${inputAln##*.}" = "sam" ]; then
    # read id file line by line
    while read -r line
    do
        # echo $line
        cleanLine=$(echo $line | sed -e 's/\r//g')
        # echo $cleanLine
        grep -F $cleanLine $inputAln
    done < "$inputId"
fi
if [ "${inputAln##*.}" = "bam" ]; then
    echo "input is BAM file, use samtools view to cut region and convert to sam file"
fi
