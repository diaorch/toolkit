#!/usr/bin/env python 

import sys

# global constants
## naming conventions: Section 1.4 https://samtools.github.io/hts-specs/SAMv1.pdf
QNAME_COL = 1 - 1
SEQ_COL = 10 - 1


def format_sam_line_to_fasta_line(line):
    fields = line.split("\t")
    cat_string = ">" + fields[QNAME_COL] + "\n" + fields[SEQ_COL]
    return(cat_string)


def main():
    """ 
    Main function: parse arguments and handles file I/O
    """
    in_filename = sys.argv[1]
    # I decided to remove the output file sys argv because
    # this can be easily redirected using bash `>`
    # out_filename = sys.argv[]

    with open(in_filename) as in_file:
        for sam_line in in_file:
            if(not sam_line.startswith("@")):
                fasta_line = format_sam_line_to_fasta_line(sam_line)
                print(fasta_line)


if __name__ == "__main__": 
    main()
