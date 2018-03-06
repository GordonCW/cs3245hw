#!/usr/bin/python
import re
import nltk
import sys
import getopt

def usage():
    print("usage: " + sys.argv[0] +\
          " -i directory-of-documents -d dictionary-file -p postings-file")

input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError as err:
    usage()
    sys.exit(2)
    
for o, a in opts:
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"
        
if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

"""
start my code here
"""

from myHelper import *

######### code start here

# get file name from the input directory
# sort file name by number
from os import listdir
from os.path import isfile, join
files = [f for f in listdir(input_directory) if isfile(join(input_directory, f))]
files.sort(key=int)

# save tuples
dictionary = []

# save DictElement
dic = {}
for file in files[:10]:
    
    with open(input_directory + '/' + file, mode="r", encoding="utf-8") as f:
        textList = f.readlines()
    
    for line in textList:
        for word in nltk.word_tokenize(line):
            if word not in string_punct:   # to get rid of single punctuation
                # make tuple for sorting
                dictionary.append( (caseFoldigAndStemming(word), int(file)) )

# sort by term
dictionary.sort(key=lambda x: x[0])

preTuple = None
for tup in dictionary:
    
    # remove duplication
    if tup != preTuple:
        
        # save the term and the docId in dic's value
        if tup[0] not in dic:
            dic[tup[0]] = DicValue( PostingList(Node(tup[1])) )
        else:
            dic[tup[0]].getPostingList().add(Node(tup[1]))
            dic[tup[0]].addOneDoc()
            
        preTuple = tup

"""
Hi Wei Qing,

Add skip pointer code here

"dic" is our final dictionary
it is also a python dictionary
the key is the term
the value is the DicValue object
dic[key].getDocFrequency() can get docFrequency
"""

## checking of posting list
#for key in dic:
#    l = dic[key].getPostingList()
#    l.resetCurrentNode()
#    h = l.getHead()
#    
#    print('count in dic value: ', dic[key].getDocFrequency())
#    count = 0
#    
#    while h != None:
#        count += 1
##        print(h.getDocId())
#        h = h.getNext()
#
#    print("real count in pl: ", count)



import pickle

# save posting list into posting.txt and then clear the memory used by those
# posting list
with open(output_file_postings, mode="wb") as f:
    
    byte_count = 0
    for term in dic:
        postingList = dic[term].getPostingList()
        encodedList = pickle.dumps(postingList)
        f.write(encodedList)
        dic[term].setPointer( (byte_count, len(encodedList)) )
        byte_count += len(encodedList)
        
        dic[term].setPostingList(None)
        
# save dic into dictionary.txt
with open(output_file_dictionary, mode="wb") as f:
    pickle.dump(dic, f)

## testing loading dic
#testingD = None
#with open(output_file_dictionary, mode="rb") as f:
#    testingD = pickle.load(f)
#
#for term in dic:
#    if dic[term].getPostingList() != testingD[term].getPostingList():
#        print("not equal ", term)
#    if dic[term].getDocFrequency() != testingD[term].getDocFrequency():
#        print("not equal ", term)
#    if dic[term].getPointer() != testingD[term].getPointer():
#        print("not equal ", term)
    
## checking for loading a posting list
#with open(output_file_postings, mode="rb") as f:
#    p = dic['to'].getPointer()
#    f.seek(p[0])
#    d = pickle.loads(f.read(p[1]))
#    
#    # see the posting list
#    h = d.getHead()
#    print('count in dic value: ', dic['to'].getDocFrequency())
#    count = 0
#    
#    while h != None:
#        count += 1
#        print(h.getDocId())
#        h = h.getNext()
#        
#    print("real count in pl: ", count)

    

# My notes
    
# tokenizing
# case-folding
# stemming

# sorting by terms

# count frequency and make posting list

# add skip pointers in posting list

# save posting list in a txt file by pickle
# save dictionary in a txt file