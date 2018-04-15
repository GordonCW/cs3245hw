#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 15:07:11 2018

@author: weiqing
"""
import re
import nltk
import sys
import getopt


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
        input_directory = a
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
TEST_OVER_NO_OF_DOC = 1

# map colunms name to the index
colIndex = {}

dictList = []
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
        docId = int(row[ colIndex['document_id'] ])
        docContent = row[ colIndex['content'] ]
        
        if '//<!\[' in docContent:
            contentSplit = docContent.split('//<![', 1)
            if len(contentSplit[0]) == 0:
                contentSplit = contentSplit[1].split('//]]>', 1)
        
                docContent = contentSplit[1]
            else:
                docContent = contentSplit[0]
            
        # remove puntuation, tokenizing, case folding and stemming
        tokens = [word for word in nltk.word_tokenize(docContent.translate(table))]
        initTerms = [caseFoldigAndStemming(token) for token in tokens]
        terms = []
        for term in initTerms:
            if "–" in term or term == '—':
                continue
            else:
                terms.append(term)

        # add unigram into lis
        for term in terms:
            dictList.append((term, docId))
        
        # add bigram into lis
        if len(terms) >= 2:
            for i in range(len(terms)-1):
                dictList.append((terms[i]+' '+terms[i+1], docId))
        
        # add trigram into lis
        if len(terms) >= 3:
            for i in range(len(terms)-2):
                dictList.append((terms[i]+' '+terms[i+1]+' '+terms[i+2], docId))

        # limit the size of corpus for testing
        if counter == TEST_OVER_NO_OF_DOC:
            break

dictList.sort(key=lambda x: x[0])



print(dictList)


df = pd.read_csv(dataset_file)
print(df)
#
##tempDf = df[df['content'].str.contains('//<!\[')]
#df['containsCode'] = df['content'].str.contains('//<!\[')
#
#print(df.dtypes)
#
#
#counter = 0
#contentSplitLen = []
#for index, row in df.iterrows():
#    print(counter)
#    counter += 1
#    docContent = None
#    if row['containsCode'] == True:
#        contentSplit = row['content'].split('//<![', 1)
#        if len(contentSplit[0]) == 0:
#            contentSplit = contentSplit[1].split('//]]>', 1)
#    
#            docContent = contentSplit[1]
#        else:
#            docContent = contentSplit[0]
#    else:
#        docContent = row['content']
#        
#    putDocIntoList(dictList, docContent, row['document_id'])
##    print(dictList)
##    sys.exit(-1)
#
#print(dictList)

        

#for row in df:
#    print(row)





#print(tempDf['document_id'])
#print("hello")
#tempDf = tempDf['document_id']
#listDf = tempDf.values.T.tolist()
##convert into list
#if(401233150 in listDf):
#    print("hello we")
    
    