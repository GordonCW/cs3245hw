#!/usr/bin/python
import re
import nltk
import sys
import getopt


def usage():
    print("usage: " + sys.argv[0] +
          " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")


dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError as err:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None:
    usage()
    sys.exit(2)


from myHelper import *


import heapq


def calculateQueryLogTF(q):
    tempList = []
    tempQueryDic = {}

    # remove terms that not in dic
    for term in q:
        if term in dic:
            tempList.append(term)

        # else do not save

    # nothing to query
    if len(tempList) == 0:
        return None

    tempList.sort()

    # count term frequency in query
    for term in tempList:
        if term not in tempQueryDic:
            tempQueryDic[term] = 1
        else:
            tempQueryDic[term] += 1

    # compute ltf
    for term in tempQueryDic:
        tempQueryDic[term] = 1 + math.log(tempQueryDic[term], 10)

    return tempQueryDic


def multiplyIDF(tempQueryDic):
    if tempQueryDic == None:
        return None
    for term in tempQueryDic:
        # term must be in dic since checked in last function
        tempQueryDic[term] *= math.log(N / dic[term].getDocFrequency(), 10)

    return tempQueryDic


def cosineScore(q):
    # compute weighted tf_t,q
    queryDic = calculateQueryLogTF(q)
    queryDic = multiplyIDF(queryDic)

    # nothing to query
    if queryDic == None:
        return None

    # init scores
    scores = [[i, None] for i in range(len(docIds))]

    # compute dot product
    for term in queryDic:
        # load posting list
        pl = getPostingList(postings_file, dic[term])
        h = pl.getHead()

        # iterate through the posting list
        while h != None:
            # retrieve the corresponding index in scores array
            tempDocId = h.getDocId()
            indexInScores = docIdToIndexMap[tempDocId]

            if scores[indexInScores][1] == None:
                scores[indexInScores][1] = h.getTermFrequency() * queryDic[term]
            else:
                scores[indexInScores][1] += h.getTermFrequency() * queryDic[term]

            h = h.getNext()

    # normalize scorse
    for x in scores:
        if x[1] != None:
            x[1] /= lengthOfDocument[docIds[x[0]]][1]

    # compute a list of tuple consisting of a nonNone-score docId and its score
    nonzeroScoresList = [(x[0], x[1]) for x in scores if x[1] != None]

    result = None
    if len(nonzeroScoresList) > 10:
        result = heapq.nlargest(10, nonzeroScoresList, key=lambda x: x[1])
    else:
        result = nonzeroScoresList.sort(key=lambda x: x[1], reverse=True)

    # return the real docIds
    return [docIds[x[0]] for x in result]


# code start here

dic = None
lengthOfDocument = None

with open(dictionary_file, mode="rb") as f:
    dic = pickle.load(f)

with open("docLength.txt", mode="rb") as f:
    lengthOfDocument = pickle.load(f)

docIds = list(lengthOfDocument.keys())
docIds.sort()
N = len(docIds)
docIdToIndexMap = {}
for i in range(len(docIds)):
    docIdToIndexMap[docIds[i]] = i

# read queries and process it
# write it back to the result file
with open(file_of_output, "w", encoding="utf-8") as t:
    with open(file_of_queries, "r", encoding="utf-8") as f:
        data = f.readlines()
        for query in data:
            query = query.rstrip("\n")
            query = nltk.word_tokenize(query)
            query = [caseFoldigAndStemming(token) for token in query]

            queryResult = cosineScore(query)
            if queryResult == None:
                t.write('\n')
            else:
                t.write(' '.join(str(x) for x in queryResult) + '\n')
