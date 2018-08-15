#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 13:54:46 2018

@author: s1680791
"""

from __future__ import unicode_literals
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--input', '-i', type=str, help='The name of the file to be processed with ezafe')

args = parser.parse_args()


def FindEzafe(line):
    ezafe_added = []
    for word in line.split():
        # ignore words that are two characters or fewer, they are complementisers or abbreviations
        if len(word) <= 2:
            ezafe_added.append(word)
        elif word[-1] == 'и':
            # concatenate 'e' to words that have ezafe
            ezafe_added.append(word + ' [e]')
        else:
            # do not change words without ezafe
            ezafe_added.append(word)
    return ezafe_added


def Reformat(line):
    list_form = FindEzafe(line)
    string_form = ' '.join(list_form)
    return string_form


def Ezafeify_Whole_File():
    infile_name = args.input
    outfile_name = infile_name + '.ezafe'
    with open(infile_name, 'r') as infh, open(outfile_name, 'w') as outf:
        for line in infh:
            new_line = Reformat(line)
            outf.write(new_line + os.linesep)
    infh.close()
    outf.close()
    return True


if args.input != None:
    Ezafeify_Whole_File()
else:
    print('ERROR: No input file specified')

