#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 15:07:11 2018

@author: weiqing
"""
import re
import getopt
import csv

from myHelper import *


def usage():
    print("usage: " + sys.argv[0] +
          " -i dataset_file -d dictionary-file -p postings-file")


dataset_file = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError as err:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i':  # input directory
        dataset_file = a
    elif o == '-d':  # dictionary file
        output_file_dictionary = a
    elif o == '-p':  # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if dataset_file == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

"""
start my code here
"""

sys.setrecursionlimit(25000)
csv.field_size_limit(100000000)
TEST_OVER_NO_OF_DOC = 3

# map colunms name to the index
colIndex = {}
dictList = []

# our final dictionary
dic = {}
contentForTesting = []
with open(dataset_file, newline='') as f:
    # [17153 rows x 5 columns]
    reader = csv.reader(f)

    # skip header
    header = next(reader)

    # map colunms name to the index
    for i in range(len(header)):
        colIndex[header[i]] = i

    counter = 0
    for row in reader:
        print(counter)
        counter += 1
        docId = int(row[colIndex['document_id']])
        docContent = row[colIndex['content']]

        # remove the junk in the content
        if '//<!\[' in docContent:
            contentSplit = docContent.split('//<![', 1)
            if len(contentSplit[0]) == 0:
                contentSplit = contentSplit[1].split('//]]>', 1)

                docContent = contentSplit[1]
            else:
                docContent = contentSplit[0]

        contentForTesting.append(docContent)
        
        tokens = []
        
        # tokenize and remove all puntuations in the content
        for words in nltk.word_tokenize(docContent):
            words = words.translate(table)
            for word in words.split(' '):
                if len(word) > 0:
                    tokens.append(word)
        
        # casefolding and stemming
        initTerms = [caseFoldigAndStemming(token) for token in tokens]
        terms = []
        for term in initTerms:
            if '–' in term or term == '–':
                continue
            else:
                terms.append(term)
#        terms = initTerms
    
        # add unigram into dictList
        for term in terms:
            dictList.append((term, docId))
        
        # add bigram into dictList
        if len(terms) >= 2:
            for i in range(len(terms)-1):
                dictList.append((terms[i]+' '+terms[i+1], docId))
        
        # add trigram into dictList
        if len(terms) >= 3:
            for i in range(len(terms)-2):
                dictList.append((terms[i]+' '+terms[i+1]+' '+terms[i+2], docId))

        # limit the size of corpus for testing - should be commented later
        if counter == TEST_OVER_NO_OF_DOC:
            break

dictList.sort(key=lambda x: x[0])


#for content in contentForTesting:
#    print([content])
#    print()


# step 6
# for each term and document, compute the tf
for term, docId in dictList:

    if term not in dic:
        dic[term] = DicValue(PostingList(Node(docId)))
    else:
        # exist in the dic
        currNode = dic[term].getPostingList().getCurrentNode()
        previousDocId = currNode.getDocId()

        # different docId
        if previousDocId != docId:
            dic[term].getPostingList().add(Node(docId))
            dic[term].addOneDoc()
        else:
            currNode.incrementTermFrequency()


# step 7
# pre compute log term frequency for searching later
for term in dic:
    pl = dic[term].getPostingList()
    h = pl.getHead()

    # iterate through the posting list
    while h != None:
        h.calculateLogTF()
        h = h.getNext()


# step 8
# pre compute the document vector length for searching later
# value is a list. the first one consider all term in dic
# the second one consider only unigram in dic
lenOfDocVector = {}
for term in dic:
    pl = dic[term].getPostingList()
    h = pl.getHead()
    while h != None:
        docId = h.getDocId()
        squaredTF = h.getTermFrequency() * h.getTermFrequency()
        if docId not in lenOfDocVector:
            lenOfDocVector[docId] = [squaredTF, 0]
        else:
            lenOfDocVector[docId][0] += squaredTF

        # check if it is unigram
        if ' ' not in term:
            lenOfDocVector[docId][1] += squaredTF
        h = h.getNext()

# computer entry-wise sqrt for lenOfDocVector
for d in lenOfDocVector:
    lenOfDocVector[d][0] = math.sqrt(lenOfDocVector[d][0])
    lenOfDocVector[d][1] = math.sqrt(lenOfDocVector[d][1])


# for testing query later
with open("terms.txt", mode="w") as f:
    for term in dic:

        pl = dic[term].getPostingList()
        h = pl.getHead()
        docIds = []
        while h != None:
            docIds.append(h.getDocId())
            h = h.getNext()
        f.write('"'+term+'"'+': '+' '.join(str(d) for d in docIds)+'\n')

# save posting list into posting.txt and then clear the memory used by those
# posting list
with open(output_file_postings, mode="wb") as f:

    byte_count = 0
    for term in dic:
        postingList = dic[term].getPostingList()
        encodedList = pickle.dumps(postingList)
        f.write(encodedList)

        # location of posting list and how many bytes to save it
        dic[term].setPointer((byte_count, len(encodedList)))
        byte_count += len(encodedList)

        dic[term].setPostingList(None)

# save dic into dictionary.txt
with open(output_file_dictionary, mode="wb") as f:
    pickle.dump(dic, f)

# save length into docLength.txt
with open("docLength.txt", mode="wb") as f:
    pickle.dump(lenOfDocVector, f)
