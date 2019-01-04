#!/usr/bin/env python3

"""
This script is to:
Modify reads in zipped fastq files to a fixed length by removing bases on the 5-prime and/or 3-prime ends

USAGE: 
python3 cropFastqReadToLength.py --mode --length <inputFastqGz> <outputFastqGz>

EXAMPLE:
python3 cropFastqReadToLength.py -m 30 test.barcode.fastq.gz test.barcode.min30.fastq.gz

DEPENDENCIES: 
Biopython

INPUT: a gzip FASTQ file

OUTPUT:
printed into given output file name: a gzipped fastq file with 

DEFAULTS:
With on input, MINSCORE would be set to 30. According to Phred+33, a score of 30 means the probability that the corresponding base call is incorrect is 10^(-3).  
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

def checkHighQual(qualString, minScore = 30):
    """
    This function checks if the all bases in given quality string 
    no less than the given minimum score
    Scoring scheme for FASTQ: Illumina 1.8+ Phred+33, [0, 41]
    Input:  
        qualString: a quality string from FASTQ file 
        minScore: a minimum score threshold as input
    Returns:
        a boolean: True when all bases quality string pass 
                   filtering, False otherwise
    """
    # encoding for qual >= 30: ?@ABCDEFGHIJ
    qualScores = '!\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJ'
    highQualScores = qualScores[minScore: ]
    index = 0
    highQualFlag = True
    qualList = list(qualString)
    while(index < len(qualString) and highQualFlag):
        if qualList[index] not in highQualScores:
            highQualFlag = False
        index += 1
    return highQualFlag 

def parseArguments():
    """
    this function parses mandatory and optional arguments from 
    scrip call
    help from: https://stackoverflow.com/a/28479869
    """
    # Create argument parser
    parser = argparse.ArgumentParser()
    # Optional arguments
    parser.add_argument('-k', '--keep-end', 
                        type = str, default = 'L', 
                        help = 'Left (L) or right (R) of the ' + 
                               'input reads should be kept and ' + 
                               'written to output; default: L')
    parser.add_argument('-n', '--keep-length', 
                        type = int, 
                        help = 'Number of bases that need to be ' + 
                               'kept and written to output file')
    # Positional mandatory arguments
    parser.add_argument('fqgz', type = str, 
                        help = 'File name of input .fastq.gz file')
    parser.add_argument('outfile', type = str, 
                        help = 'File name of output .fastq.gz file')
    # Print version
    parser.add_argument('--version', action='version', 
                        version='%(prog)s - Version 0.1')
    # Parse arguments
    args = parser.parse_args()
    return args

def main(fqInputName, outputName, minScore):
    with gzip.open(outputName, 'wb') as outHandle:
        with gzip.open(fqInputName, 'rt') as inHandle:
            for title, seq, qual in FastqGeneralIterator(inHandle):
                if checkHighQual(qual, minScore = minScore):
                    outEntry = '@' + title + '\n' + seq + '\n+\n' + qual + '\n'
                    outHandle.write(outEntry.encode())

if __name__ == '__main__':
    args = parseArguments()
    print(args.fqgz)
    print(args.outfile)
    print(args.keep_end)
    print(args.keep_length)
    # main(fqInputName = args.fqgz, 
    #      outputName = args.outfile, 
    #      minScore = args.minScore) 
    
