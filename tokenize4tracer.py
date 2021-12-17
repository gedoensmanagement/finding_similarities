#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Prepares a txt file for TRACER (i.e. normalization and tokenization). 
    Returns a tsv file.
    You need to replace the placeholders "XX" in the first column before feeding it to TRACER! 
    
    Created 2021-03-04 by muellerM@ieg-mainz.de. """


import re
import sys
from pathlib import Path
import argparse
from datetime import datetime

def init_argparse():
    """ Returns a parser that processes the arguments from the command line. """
    parser = argparse.ArgumentParser(
            usage="%(prog)s [FILE1.txt]",
            description=""" Prepares (i.e. tokenizes) a txt file for TRACER. 
                            Returns a tsv file.
                            You need to replace the placeholders "XX" in the first column before feeding it to TRACER! """
        )

    parser.add_argument(
            "-p", "--placeholder", default="XX", 
            help="The first to digits in the first column indicate the file in the tsv for TRACER. You can define these digits here or use 'XX' as a placeholder that is replaced later. DEFAULT = XX"
        )
    
    parser.add_argument(
            "-a", "--addition", default=False,
            help="Addition to the file name that identifies e.g. a certain chapter."
        )

    parser.add_argument(
            "-o", "--output_folder", default="output",
            help='Directory containing the output file. Default = "output".'
        )

    parser.add_argument(
            "file", nargs=1, type=str,
        )
    
    return parser


def normalize(data):
    """ Eats text. Replaces special characters by convertign them to normal 
        characters, spaces or nothing. Returns text. """
    # Special characters to be replaced when normalizing the text:
    replacement_table = {
        '[àáâ]': 'a',
        '[èéêë]': 'e',
        '[ìíîï]': 'i',
        '[òóô]': 'o',
        '[ùúûv]': 'u',
        '[æę]': 'ae',
        'V': 'U',
        'j': 'i',
        'J': 'J',
        'Æ': 'Ae',
        'œ': 'oe',
        'Œ': 'Oe',
        '&c\.': 'etc.',     # etc.
        '&': 'et',
        '\r\n': '\n',       # convert Windows line breaks to Linux line breaks
        '^\n$': '',         # empty lines
        '\[.*?\]': '',      # [Col. XXXX] in Rupertus Tuitiensis
        '\sn\d{1,4}': '',   # notes in Rupertus Tuitiensis
        '---': ' ',         # separator in Rupertus Tuitiensis
        '\s\d{1,4}\s': ' ', # page numbers in Rupertus Tuitiensis
        '[«»]': '',         # citations in Rupertus Tuitiensis
        }

    for pattern, replacement in replacement_table.items():
            data = re.sub(pattern, replacement, data)
    return data

def save_abbreviations(data):
    """ Eats text. 
        Makes sure that special abbreviations like "Cap. II" or "Ioan. XI" 
        will be preserved (and not splitted by tokenization because they
        contain a full stop followed by a capital letter). 
        Returns text. """
    # Build patterns that match the books of the bible and some common abbreviations:
    ## abbreviations for biblical books:
    pattern_books = "1Cor|1Ioh|1Joh|1Kor|1Macc|1Par|1Petr|1Reg|1Sam|1Thess|2Cor|2Ioh|2Joh|2Kor|2Macc|2Par|2Petr|2Reg|2Sam|2Thess|3Ioh|3Joh|Abd|Act|Actor|Ag|Agg|Amos|Apc|Apoc|Bar|Baruch|Can|Cant|Cap|Col|Colos|Coloss|Dan|Daniel|Deut|Deuter|Deuteronomium|Dt|Ec|Ecc|Eccl|Eccle|Eccli|Eph|Ephes|Esa|Esd|Esdr|Esdrae|Est|Esth|Esther|Ex|Exod|Exodus|Eze|Ezech|Gal|Galat|Gen|Genes|Genesis|Hab|Habac|Hag|Hebr|Hezek|Hos|I Cor|II Cor|Iac|Iak|Ier|Ioan|Iob|Ioel|Ioh|Ion|Iona|Ios|Iosue|Isa|Isai|Iud|Iud|Iudic|Iudicum|Jac|Jak|Joan|Job|Joel|Joh|Jon|Jona|Jos|Josue|Jer|Jerem|Jes|Jud|Judic|Kor|Lam|Lament|Leu|Leuit|Leuiticus|Lev|Leviticus|Lucae|Luc|Mac|Macc|Mach|Machab|Mal|Malac|Malach|Marc|Matth|Mic|Mich|Nah|Nahum|Neh|Nehem|Nehemiae|Num|Numer|Numeri|Obadja|Os|Ose|Par|Para|Paral|Paralip|Petr|Phil|Philip|Philipp|Pro|Prou|Prov|Ps|Psa|Psal|Psalm|Qo|Qoh|Reg|Regum|Ro|Rom|Roma|Rut|Ruth|Sam|Sap|Sapient|Soph|Thes|Thess|Tho|Thobis|Tim|Tit|Tob|Thren|Zach|Zef|Zeph"
    ## general Latin abbreviations:
    pattern_books += "|cap|CAP|lib|ib|ibid|Ibid|sc|tom"
    ## Latin numerals:
    pattern_books = f"({pattern_books})\.?\s([CLXIVU0-9])"    
        
    data = re.sub(pattern_books, "\g<1>.\g<2>", data)
    return data

def tokenize(data):
    """ Eats text. Tokenizes the text by inserting line breaks. 
        Returns text (with tokens separated by line breaks). """
    token_separators = {
        '([:;\?\!])\s': '\g<1>\n',
        '\.\s([A-Z])': '.\n\g<1>',
    }

    for pattern, replacement in token_separators.items():
        data = re.sub(pattern, replacement, data)
    return data

def get_bibtex(filename):
    """ Tries to extract a bibtex key from a filename and returns it.
        If no bibtex key is found the function returns the filename (without suffix). """

    bibtex = re.match(r'^[a-zA-Z]*\d{4}[a-z]?', Path(filename).stem)
    if bibtex:
        bibtex = bibtex.group()
    else:
        bibtex = Path(filename).stem
    return bibtex

def get_addition(filename):
    """ Tries to extract the filename addition that indicates which part of an opus
        we are dealing with, e.g. Wild1550,_Joh6_,,,,2021-03-15T20-52-14.tsv → _Joh6_ """
    try:
        addition = filename.split(",")[-4]
    except:
        sys.exit("\nERROR Could not find a filename addition that indicates which part of an opus we are dealing with. Please provide a filename addition using the '-a' option!'")

    if addition.startswith("_") and addition.endswith("_"):
        return addition
    else:
        return False
    

def convert_to_tracer(file, placeholder):
    """ Eats a filename of a text file. 
        Normalizes and tokenizes the text.
        Converts it to tsv in the TRACER input format.
        Writes the tsv file. 
        Depends on normalize(), save_abbreviations() and tokenize(). """
        
    with open(Path(file), "r", encoding="utf-8") as f:
        data = f.read()
        #matches = re.findall('\sn\d{1,4}', data)
        data = normalize(data)
        data = save_abbreviations(data)
        data = tokenize(data)
    
        bibtex = get_bibtex(file)
        
        output = []
        i = 1
        for line in data.split("\n"):
            if line != "" and len(line.split(" ")) > 2:
                line = placeholder + f"{i:05}\t" + line.strip() + f"\tNULL\t{bibtex}\n"
                output.append(line)
                i += 1

    return output

def main():
    parser = init_argparse()
    args = parser.parse_args()
    file = args.file[0]
    placeholder = args.placeholder
    new_addition = args.addition
    output_folder = args.output_folder
    
    print(f"Tokenizing {file} ...")
    output = convert_to_tracer(file, placeholder)
    
    bibtex = get_bibtex(Path(file).stem)
    timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

    if new_addition:
        addition = new_addition
    elif get_addition(Path(file).stem):
        addition = get_addition(Path(file).stem)
        print(f"INFO  Found an addition that indicates the opus: {addition}")
    else:
        addition = ""

    outfile = f"{bibtex},{addition},,,{timestamp}.tsv" # Commas are needed to preserve compatability with the tsv files generated on the server!
    if output_folder != "":
        outfile = f"{output_folder}/{outfile}"

    with open(Path(outfile), "w", encoding="utf-8") as o:
        o.writelines(output)
    print(f"Finished! Output written to {outfile}.")
    if placeholder == "XX":
        print('Remember to replace the placeholders "XX" in the first column before feeding the file to TRACER!')

if __name__ == "__main__":
    main()
