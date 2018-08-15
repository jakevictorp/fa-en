#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 13:54:46 2018

@author: s1680791
"""


from __future__ import unicode_literals
from hazm import *
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--input', '-i', type=str, help='The name of the file to be processed with ezafe')

args = parser.parse_args()

#normalizer = Normalizer()
#
#
#stemmer = Stemmer()
#
#
#lemmatizer = Lemmatizer()


tagger = POSTagger(model='resources/postagger.model')


def AddEzafe(line):
    ezafe_added = []
    fully_tagged = tagger.tag(word_tokenize(line))
    for word in fully_tagged:
        #check if the last character of the tag is 'e', indicating ezafe
        if word[1][-1] == 'e':
            #add [e] after words that have ezafe
            ezafe_added.append(word[0]+' [e]')
        else:
            #do not change words without ezafe
            ezafe_added.append(word[0])
    return ezafe_added


def Reformat(line):
    list_form = AddEzafe(line)
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
    

#
#
#chunker = Chunker(model='resources/chunker.model')
#
#tree2brackets(chunker.parse(tagged))
#
#parser = DependencyParser(tagger=tagger, lemmatizer=lemmatizer)


