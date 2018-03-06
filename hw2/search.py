#!/usr/bin/python
import re
import nltk
import sys
import getopt

def usage():
    print("usage: " + sys.argv[0] + \
    " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")

dictionary_file = postings_file = file_of_queries = output_file_of_results = None
	
try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError as err:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file  = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None :
    usage()
    sys.exit(2)
    

from myHelper import *
"""
Hi Wei Qing,

implement the Shunting-yard algorithm here
"""

# functions defined by Gordon

def AND(postingList1, postingList2):
    if term1 not in dic or term2 not in dic:
        return None


# load dic back into memory
dic = None
with open(dictionary_file, mode="rb") as f:
    dic = pickle.load(f)
    
"""
Hi Wei Qing,

load query here
"""