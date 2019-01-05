#!/usr/bin/env python3

"""
This script is to:
Modify reads in zipped fastq files to a fixed length by removing bases on the 5-prime and/or 3-prime ends

USAGE: 
python3 cropFastqReadToLength.py (-L|-R) --keep-length/-n N <inputFastqGz> <outputFastqGz>

EXAMPLE:
python3 cropFastqReadToLength.py -L --keep-length 5 test.fastq.gz test.cropped.fastq.gz

DEPENDENCIES: 
Biopython

ARGS:
-L|-R: to keep left or right end of the sequences
--keep-length/-n N: to keep N bases at the desired end

INPUT: 
a gzip FASTQ file

OUTPUT:
printed into given output file name: a gzipped fastq file with 

DEFAULTS:
-L, i.e. keeping the left end of sequences
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import gzip
import Bio
from Bio.SeqIO.QualityIO import FastqGeneralIterator
# from Bio import SeqIO
import argparse

def cropString(string, keepLeft, keepRight, keepLen = 0):
    """
    This function crop a given string to desired length by keeping only 
    characters from desired end.
    Args:
        string: Character string to be crop.
        keepEnd: Which end of string to be kept, can be either of:
                 'L' (default) left, 'R' right
        keepLen: The desired length of result cropped sequence. 
    Returns:
        
    Raises:
        KeyError: Raises an exception
    """
    # # catch exception when input string indicating which end to keep is 
    # # neither 'L' (keep left end) nor 'R' (keep right end)
    # if (keepEnd != 'L' and keepEnd != 'R'):
    #     raise ValueError('--keep-end/-k must be either \'L\' or \'R\'')
    if (keepLen <= 0):
        raise ValueError('--keep-length/-n must be a positive integer')
    if (keepLeft): 
        keepEnd = 'L'
    elif (keepRight):
        keepEnd = 'R'
    # crop sequence
    if (keepEnd == 'L'):
        c = string[0:keepLen]
    else:
        c = string[-keepLen:]
    return c 

def parseArguments():
    """
    this function parses mandatory and optional arguments from 
    scrip call
    help from: https://stackoverflow.com/a/28479869
    """
    # Create argument parser
    parser = argparse.ArgumentParser()
    # mutually exclusive arguments
    keep_end = parser.add_mutually_exclusive_group(required = True)
    keep_end.add_argument('-L', '--left', 
                          action = 'store_true', default = False, 
                          help = 'Keep and write the left end of sequence')
    keep_end.add_argument('-R', '--right', 
                          action = 'store_true', default = False, 
                          help = 'Keep and write the right end of sequence')
    # Positional mandatory arguments
    parser.add_argument('-n', '--keep-length', 
                        type = int, required = True, 
                        help = 'Number of characters to keep' + 
                               'and write to output file')
    parser.add_argument('infile', type = str, 
                        help = 'File name of input .fastq.gz file')
    parser.add_argument('outfile', type = str, 
                        help = 'File name of output .fastq.gz file')
    # Print version
    parser.add_argument('--version', action='version', 
                        version='%(prog)s - Version 0.1')
    # Parse arguments
    args = parser.parse_args()
    return args

def main(inputName, outputName, keepLeft, keepRight, keepLen):
    with gzip.open(outputName, 'wb') as outHandle:
        with gzip.open(inputName, 'rt') as inHandle:
            for title, seq, qual in FastqGeneralIterator(inHandle):
                c = cropString(string = seq, 
                               keepLeft = keepLeft, keepRight = keepRight, 
                               keepLen = keepLen)
                q = cropString(string = qual, 
                               keepLeft = keepLeft, keepRight = keepRight, 
                               keepLen = keepLen)
                outEntry = '@' + title + '\n' + c + '\n+\n' + q + '\n'
                outHandle.write(outEntry.encode())

if __name__ == '__main__':
    args = parseArguments()
    
    # if (not(args.left or args.right)):
    #     raise ValueError('Either -L or -R should be supplied to ' + 
    #                      'indicate which end of the sequences to keep.')
    # elif (args.left and args.right):
    #     raise ValueError('Only one of -L or -R should be supplied to ' + 
    #                      'indicate which end of the sequences to keep.')
        
    main(inputName = args.infile, outputName = args.outfile, 
         keepLeft = args.left, keepRight = args.right, 
         keepLen = args.keep_length)
