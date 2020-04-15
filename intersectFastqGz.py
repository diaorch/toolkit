#!/usr/bin/env python3

"""
This script is to:
take two fastq.gz files and output the intersect reads as a fastq.gz file

USAGE:
python3 intersectFastqGz.py [-rc] -x inputFileX.fastq.gz -y inputFileY.fastq.gz -o outputFile.fastq.gz

EXAMPLE:

DEPENDENCIES:
Biopython

ARGS:
-x: file name for first input fastq.gz file
-y: file name for second input fastq.gz file
-rc: if provided, compare sequences in file x to the reverse complement of sequences file y, instead sequences in file y
-o: file name for output fastq.gz file that stores only intersect reads from file x and y 

INPUT: 
2 fastq.gz files

OUTPUT:
1 fastq.gz file with only intersect reads of inputs 

DEFAULTS:
None
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import gzip
import Bio
from Bio.SeqIO.QualityIO import FastqGeneralIterator
from Bio.Seq import reverse_complement
import argparse

def parseArguments():
    """
    this function parses arguments from script call
    help from: https://stackoverflow.com/a/28479869
    """
    # create argument parser
    parser = argparse.ArgumentParser()
    # positional mandatory arguments
    parser.add_argument('-x', type = str, required = True, 
                        help = 'First file to take intersect from')
    parser.add_argument('-y', type = str, required = True, 
                        help = 'Second file to take intersect from')
    parser.add_argument('-rc', action = 'store_true')
    parser.add_argument('-o', type = str, required = True, 
                        help = 'Output file of intersect reads')
    # parse arguments
    args = parser.parse_args()
    return args

def formatEntry(title, seq):
    s = title.split(' ')[0] + seq
    return s

def main(x, y, rc, o):
    """
    parse gz file and unzipped fastq file and find intersection
    """
    xSet = set()
    with gzip.open(x, 'rt') as xHandle:
        for title, seq, qual in FastqGeneralIterator(xHandle):
            # print(title)
            # print(title.split(' ')[0])
            # print(formatEntry(title, seq))
            xSet.add(formatEntry(title, seq))
    with gzip.open(o, 'wb') as outHandle:
        with gzip.open(y, 'rt') as yHandle:
            for title, seq, qual in FastqGeneralIterator(yHandle):
                if rc:
                    s = reverse_complement(seq)
                c = formatEntry(title, s)
                if c in xSet: 
                    outEntry = '@' + title + '\n' + s + '\n+\n' + qual + '\n'
                    outHandle.write(outEntry.encode())
    

if __name__ == '__main__':
    args = parseArguments()
    main(x = args.x, y = args.y, rc = args.rc, o = args.o)


