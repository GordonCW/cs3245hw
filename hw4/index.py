#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 15:07:11 2018

@author: weiqing
"""
import re
import getopt
import csv
from collections import Counter

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

"""
our final dictionary
key is term
value is a list of list
where the first entry is doc frequency
the second is a list of tuple in the form of (docId, tf)
"""
dic = {}
#contentForTesting = []
with open(dataset_file, newline='', encoding="utf-8") as f:
    # [17153 rows x 5 columns]
    reader = csv.reader(f)

    # skip header
    header = next(reader)
#    print(header)

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

#        contentForTesting.append(docContent)
        
        # tokenize and remove all puntuations in the content
        tokens = []
        for words in nltk.word_tokenize(docContent):
            words = words.translate(table)
            for word in words.split(' '):
                if len(word) > 0:
                    tokens.append(word)
        
        # casefolding and stemming
        initTerms = [caseFoldigAndStemming(token) for token in tokens]
        unigramTerms = []
        for term in initTerms:
            if '–' in term or term == '–' or term in stopwords:
                continue
            else:
                unigramTerms.append(term)

        otherTerms = []
        
        # add bigram
        if len(unigramTerms) >= 2:
            for i in range(len(unigramTerms)-1):
                otherTerms.append(unigramTerms[i]+' '+unigramTerms[i+1])
        
        # add trigram into dic
        if len(unigramTerms) >= 3:
            for i in range(len(unigramTerms)-2):
                otherTerms.append(unigramTerms[i]+' '+unigramTerms[i+1]+' '+\
                    unigramTerms[i+2])

        terms = Counter(unigramTerms)
        terms.update(otherTerms)

        for term in terms:
            # weighted
            w = 1 + math.log(terms[term], 10)
            if term not in dic:
                dic[term] = [1, [(docId, w)]]
            else:
                dic[term][0] += 1
                dic[term][1].append( (docId, w) )

#        # limit the size of corpus for testing - should be commented later
#        if counter == TEST_OVER_NO_OF_DOC:
#           break


# pre compute the document vector length for searching later
# value is a list. the first one consider all term in dic
# the second one consider only unigram in dic
lenOfDocVector = {}
for term in dic:
    for docId, w_tf in dic[term][1]:
        squared = w_tf * w_tf
        if docId not in lenOfDocVector:
            lenOfDocVector[docId] = [squared, 0]
        else:
            lenOfDocVector[docId][0] += squared

        # check if it is unigram
        if ' ' not in term:
            lenOfDocVector[docId][1] += squared

# computer entry-wise sqrt for lenOfDocVector
for d in lenOfDocVector:
    lenOfDocVector[d][0] = math.sqrt(lenOfDocVector[d][0])
    lenOfDocVector[d][1] = math.sqrt(lenOfDocVector[d][1])


# save posting list into posting.txt and then clear the memory used by those
# posting list
with open(output_file_postings, mode="wb") as f:

    byte_count = 0
    for term in dic:
        postingList = dic[term][1]
        encodedList = pickle.dumps(postingList)
        f.write(encodedList)

        # location of posting list and how many bytes to save it
        pointer = (byte_count, len(encodedList))
        byte_count += len(encodedList)

        # the second element change from a posting list to a pointer
        dic[term][1] = pointer

# save dic into dictionary.txt
with open(output_file_dictionary, mode="wb") as f:
    pickle.dump(dic, f)

# save length into docLength.txt
with open("docLength.txt", mode="wb") as f:
    pickle.dump(lenOfDocVector, f)
