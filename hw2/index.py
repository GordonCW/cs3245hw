#!/usr/bin/python
import re
import nltk
import sys
import getopt

def usage():
    print("usage: " + sys.argv[0] +
          " -i directory-of-documents -d dictionary-file -p postings-file")


input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError as err:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i':  # input directory
        input_directory = a
    elif o == '-d':  # dictionary file
        output_file_dictionary = a
    elif o == '-p':  # postings file
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


sys.setrecursionlimit(25000)

# code start here

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

# save for later doing the NOT operation
all_docId = []
for file in files:
    all_docId.append(int(file))

    with open(input_directory + '/' + file, mode="r", encoding="utf-8") as f:
        textList = f.readlines()

    for line in textList:
        for word in nltk.word_tokenize(line):
            if word not in string_punct:   # to get rid of single punctuation
                # make tuple for sorting
                dictionary.append((caseFoldigAndStemming(word), int(file)))

# sort by term
dictionary.sort(key=lambda x: x[0])

preTuple = None
for tup in dictionary:

    # remove duplication
    if tup != preTuple:

        # save the term and the docId in dic's value
        if tup[0] not in dic:
            dic[tup[0]] = DicValue(PostingList(Node(tup[1])))
        else:
            dic[tup[0]].getPostingList().add(Node(tup[1]))
            dic[tup[0]].addOneDoc()

        preTuple = tup


#create skip pointer
        
        
for term in dic:

    termFreq = dic[term].getDocFrequency()

    avgjump = average_jumps(termFreq)

    # if length is less than 3 then dont need skip pointer
    if dic[term].getDocFrequency() > 3:
        
        # start at first ID
        start = 0
        # get postingList
        pl = dic[term].getPostingList()
        # get the head of the postingList
        head = pl.getHead()

        temp = head

        while start < termFreq:
            
            for i in range(avgjump):
                temp = temp.getNext()
                if temp == None:
                    break
            # setSkipPointer
            head.setSkipNext(temp)
            # current node set to head
            head = temp
            # reset the counter
            
            start += avgjump



# save special term in dic for later implementing NOT operation
dic[special_term] = DicValue(PostingList(Node(all_docId[0])))
for i in range(1, len(all_docId)):
    dic[special_term].getPostingList().add(Node(all_docId[i]))
    dic[special_term].addOneDoc()


# save posting list into posting.txt and then clear the memory used by those
# posting list
with open(output_file_postings, mode="wb") as f:

    byte_count = 0
    for term in dic:
        postingList = dic[term].getPostingList()
        encodedList = pickle.dumps(postingList)
        f.write(encodedList)
        dic[term].setPointer((byte_count, len(encodedList)))
        byte_count += len(encodedList)

        dic[term].setPostingList(None)

# save dic into dictionary.txt
with open(output_file_dictionary, mode="wb") as f:
    pickle.dump(dic, f)
