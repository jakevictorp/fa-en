#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 14:42:03 2018

@author: s1680791
"""




from __future__ import unicode_literals
import codecs
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--input', '-i', type=str, help='The name of the corpus file to be reduced')
parser.add_argument('--number', '-n', type=int, help='The number by which the corpus is to be divided (e.g. "2" to halve it, "3" to split it into thirds, etc.)')


args = parser.parse_args()



def ShrinkCorpus():
    infile_name = args.input
    suffix = infile_name[-2:]
    prefix = infile_name[:-2]
    denom = args.number
    fraction = 'div_by_' + str(denom)
    final = prefix + fraction + '.' + suffix
    #reduce corpus by required fraction
    with open(infile_name, 'r') as infh, open(final, 'w') as fc:
        index = 0
        for line in infh:
            index += 1
            if index % denom == 0:
                fc.write(line)
            else:
                continue
    infh.close()
    fc.close()
    return True


if args.input != None:
    ShrinkCorpus()
else:
    print('ERROR: No input file specified')
