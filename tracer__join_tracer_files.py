#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 14:43:09 2021

@author: muellerM@ieg-mainz.de
"""
import argparse
import csv
from pathlib import Path
import re
import sys

def init_argparse():
    """ Returns a parser that processes the arguments from the command line. """
    parser = argparse.ArgumentParser(
            usage="%(prog)s [FILE1.tsv] [FILE2.tsv] [...]",
            description=""" Joins tsv files for TRACER that still have a placeholder in the first column. """
        )
    
    parser.add_argument(
            "-o", "--output_folder", default="output",
            help='Directory containing the output file. Default = "output".'
        )

    parser.add_argument(
            "files", nargs="+", type=str,
        )
    
    return parser

def get_bibtex(filename):
    """ Tries to extract a bibtex key from a filename and returns it.
        If no bibtex key is found the function returns the filename (without suffix). """

    bibtex = re.match(r'^[a-zA-Z]*\d{4}[a-z]?', Path(filename).stem)
    if bibtex:
        bibtex = bibtex.group()
    else:
        bibtex = Path(filename).stem
    return bibtex

def main():
    parser = init_argparse()            # create a parser
    args = parser.parse_args()          # parse the command line arguments
    files = args.files                  # get the "files" argument
    output_folder = args.output_folder  # get the "output_folder" argument
    
    outfiles = []
    
    for idx, file in enumerate(files):
        idx += 10 # The first file should have the index 10.
        output = []
        bibtex = get_bibtex(file)
        addition = file.split(",")[-4]
        with open(Path(file), "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                # Insert the index of the file into the first column:
                row[0] = f"{idx:02d}{row[0][2:]}"
                output.append(row)
        outfiles.append({'bibtex': bibtex,
                         'addition': addition,
                         'data': output})
    
    outfilename = "_vs_".join([f"{outfile['bibtex']},{outfile['addition']}" for outfile in outfiles]) + ".tsv"
    
    if sys.platform == "win32":
        if len(outfilename) > 260:
            outfilename = outfilename[:50] + ".tsv"
        
    if output_folder != "":
        outfile = f"{output_folder}/{outfilename}" 
    
    with open(Path(outfilename), "w", encoding="utf-8") as o:
        for outfile in outfiles:
            writer = csv.writer(o, delimiter="\t", quoting=csv.QUOTE_NONE)
            for row in outfile['data']:
                writer.writerow(row)
    
    print("INFO", outfilename, "successfully written.")
    
if __name__ == "__main__":
    main()
