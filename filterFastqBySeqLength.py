#!/usr/bin/env python3
"""
This script takes a fastq as input, filter to keep and write to screen only entries that have sequence length in [minLen, maxLen]
USAGE:
diaorch@serenity:~/data/cz$ python ~/projects/toolkit/filterFastqBySeqLength.py --file 10_poolPAM/17_pooled_S9-S59.cut.repeat.singleEnd.fastq --minLen 30 --maxLen 30 > 10_poolPAM/pooled.filter30.fastq
"""

import sys
import argparse

def parseFastq(fastqFilename, minLen, maxLen):
    from Bio import SeqIO
    fastqParser = SeqIO.parse(fastqFilename, 'fastq')
    wanted = (rec for rec in fastqParser if (len(rec.seq) >= minLen and len(rec.seq) <= maxLen))
    outHandle = sys.stdout
    SeqIO.write(wanted, outHandle, 'fastq')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Filter fastq by sequence length in [minLen, maxLen]')
    parser.add_argument('--file', type = str, dest = 'fastqFilename', help = 'an string specifying the filename for input fastq file')
    parser.add_argument('--minLen', type = int, dest = 'minLen', help = 'an integer for the minimum length of sequences to be kept')
    parser.add_argument('--maxLen', type = int, dest = 'maxLen', help = 'an integer for the maximum length of sequences to be kept')
    args = parser.parse_args()
    # print(args)
    # print(args.fastqFilename)
    parseFastq(fastqFilename = args.fastqFilename, minLen = args.minLen, maxLen = args.maxLen)
    
