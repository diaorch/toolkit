#!/usr/bin/env python3

"""
This script is to:
Filter out entries with ANY bases of quality scores lower than the given threshold
Uses Illumina 1.8+ Phred+33, [0, 41] encoding, 
i.e. quality encoding can only be from 0 to 41 as: !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJ

USAGE: 
python3 filterFastqByBaseQuality.py [-m MINSCORE] <inputFastqGz> <outputFastqGz>

EXAMPLE:
python3 filterFastqByBaseQuality.py -m 30 test.barcode.fastq.gz test.barcode.min30.fastq.gz
or:
python3 filterFastqByBaseQuality.py -m 30 test.barcode.fastq.gz test.barcode.min30.fastq.gz &> test.logerr

DEPENDENCIES: 
Biopython

ARGUMENTS:
name of a gzipped FASTQ file to be filtered,
a commandline input integer of minimum score allowed, 
name of a gzipped FASTQ file for filtered results

OUTPUT:
saved into given output file name: a gzipped fastq file with surviving entries of the FastQ entries (i.e. entries with all bases of quality greater than input threshold) 
screen output: 5 comma separated fields: input file name, input read count, output file name, output read count, survival rate

DEFAULTS:
With no -m input, MINSCORE would be set to 30. According to Phred+33, a score of 30 means the probability that the corresponding base call is incorrect is 10^(-3).  
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
    This function checks if the all bases in given quality string no less than 
    the given minimum score
    Scoring scheme for FASTQ: Illumina 1.8+ Phred+33, [0, 41]
    Input:  
        qualString: a quality string from FASTQ file 
        minScore: a minimum score threshold as input
    Returns:
        a boolean: 
        True when all bases quality string pass filtering, False otherwise
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
    this function parses mandatory and optional arguments from scrip call
    help from: https://stackoverflow.com/questions/28479543/run-python-script-with-some-of-the-argument-that-are-optional
    """
    # Create argument parser
    parser = argparse.ArgumentParser()
    # Optional arguments
    parser.add_argument('-m', '--minScore', 
                        type = int, default = 30, 
                        help = 'Minimum score required for each base to pass quality filtering, ranges [0, 41] by Illumina 1.8+ Phred+33')
    # Positional mandatory arguments
    parser.add_argument('fqgz', type = str, 
                        help = 'Name of input .fastq.gz file')
    parser.add_argument('outfile', type = str, 
                        help = 'Name of output filtered .fastq.gz file')
    # Print version
    parser.add_argument("--version", action="version", 
                        version='%(prog)s - Version 0.1')
    # Parse arguments
    args = parser.parse_args()
    return args

def main(fqInputName, outputName, minScore):
    with gzip.open(outputName, 'wb') as outHandle:
        with gzip.open(fqInputName, 'rt') as inHandle: 
            inCounter = 0
            outCounter = 0
            for title, seq, qual in FastqGeneralIterator(inHandle):
                inCounter += 1
                if checkHighQual(qual, minScore = minScore):
                    outEntry = '@' + title + '\n' + seq + '\n+\n' + qual + '\n'
                    outHandle.write(outEntry.encode())
                    outCounter += 1
            print(','.join([fqInputName, str(inCounter), outputName, str(outCounter), format(outCounter / inCounter, '.8f')]))

if __name__ == '__main__':
    args = parseArguments()
    main(fqInputName = args.fqgz, 
         outputName = args.outfile, 
         minScore = args.minScore) 
    
