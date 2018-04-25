#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import nltk
import sys
import getopt

from queryExpansion import *


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
        # save time for tf=1
        if tempQueryDic[term] != 1:
            tempQueryDic[term] = 1 + math.log(tempQueryDic[term], 10)

        # else do nothing as it already is correct value

    return tempQueryDic


def multiplyIDF(tempQueryDic):
    if tempQueryDic == None:
        return None
    for term in tempQueryDic:
        # term must be in dic since checked in last function
        if tempQueryDic[term] == 1:
            # save time
            tempQueryDic[term] = math.log(N / dic[term][0], 10)
        else:
            tempQueryDic[term] *= math.log(N / dic[term][0], 10)

    return tempQueryDic


def cosineScore(q, booleanQuery):
    """
    q is a list of string where each string is a unigram"""
    if len(q) == 0:
        return None

    # compute weighted tf_t,q
    queryDic = None
    if booleanQuery == True:
        queries = []
        for queryList in q:
            for query in queryList:
                queries.append(query)

        queryDic = calculateQueryLogTF(queries)
        queryDic = multiplyIDF(queryDic)
    else:
        queryDic = calculateQueryLogTF(q)
        queryDic = multiplyIDF(queryDic)

    # nothing to query
    if queryDic == None:
        return None

    # init scores for every doc
    scores = [[i, None, 0] for i in range(len(docIds))]

    # for limiting the space of searching for boolean query
    postingListForBoolean = None
    if booleanQuery == True:

        # assume there is at least one query word
        if len(q[0]) == 1:
            postingListForBoolean = \
            [ tu[0] for tu in getPostingList(postings_file, dic[q[0][0]]) ]
        else:
            postingList1 = \
            [ tu[0] for tu in getPostingList(postings_file, dic[q[0][0]]) ]
            postingList2 = \
            [ tu[0] for tu in getPostingList(postings_file, dic[q[0][1]]) ]

            postingListForBoolean = OR(postingList1, postingList2)
            for wordQ in q[0][2:]:
                tempPosting = \
                [ tu[0] for tu in getPostingList(postings_file, dic[wordQ]) ]
                postingListForBoolean = OR(postingListForBoolean, tempPosting)

        for wordList in q[1:]:
            if len(wordList) == 1:
                scope = \
                [ tu[0] for tu in getPostingList(postings_file, dic[wordList[0]]) ]
            else:
                postingList1 = \
                [ tu[0] for tu in getPostingList(postings_file, dic[wordList[0]]) ]
                postingList2 = \
                [ tu[0] for tu in getPostingList(postings_file, dic[wordList[1]]) ]

                scope = OR(postingList1, postingList2)
                for wordQ in wordList[2:]:
                    tempPosting = \
                    [ tu[0] for tu in getPostingList(postings_file, dic[wordQ]) ]
                    scope = OR(scope, tempPosting)

            postingListForBoolean = AND(postingListForBoolean, scope)

    if postingListForBoolean != None:
        print(len(postingListForBoolean))

    # compute dot product
    for term in queryDic:
        # load posting list
        # term must be in dic
        # otherwise it is removed in calculateQueryLogTF function
        pl = getPostingList(postings_file, dic[term])
        if booleanQuery == True:
            pl = ANDWithTfInFirstList(pl, postingListForBoolean)
        
        for tempDocId, w_tf in pl:
            # retrieve the corresponding index in scores array
            indexInScores = docIdToIndexMap[tempDocId]
#            print(indexInScores, term, tempDocId, h.getTermFrequency(), queryDic[term])

            if scores[indexInScores][1] == None:
                scores[indexInScores][1] = w_tf * queryDic[term]
                scores[indexInScores][2] += 1
            else:
                scores[indexInScores][1] += w_tf * queryDic[term]
                scores[indexInScores][2] += 1

    # normalize scorse by the corresponding weighted doc vector length
    for x in scores:
        if x[1] != None:
            x[1] /= lengthOfDocument[ docIds[x[0]] ][1]

    # compute a list of tuple consisting of a nonNone-score docId and its score
    if booleanQuery == True:
        nonzeroScoresList = [(x[0], x[1]) for x in scores if x[1] != None]
    else:
        nonzeroScoresList = [(x[0], x[1]) for x in scores if x[1] != None and x[2] >= math.ceil(ORIGINAL_NO-1)]
        print("Threshold:", math.ceil(ORIGINAL_NO-1))
    nonzeroScoresList.sort(key=lambda x: x[1], reverse=True)
    result = nonzeroScoresList

    # result = None
    # if len(nonzeroScoresList) > 10:
    #     result = heapq.nlargest(10, nonzeroScoresList, key=lambda x: x[1])
    # else:
    #     result = nonzeroScoresList.sort(key=lambda x: x[1], reverse=True)

    # return the real docIds
    return [docIds[x[0]] for x in result]


def AND(postingList1, postingList2):
    # print(postingList1)
    # print(postingList2)
    if len(postingList1) == 0 or len(postingList2) == 0:
        return []
    result = []

    i1 = 0
    i2 = 0
    p1Length = len(postingList1)
    p2Length = len(postingList2)
    while i1 < p1Length and i2 < p2Length:
        p1DocId = postingList1[i1]
        p2DocId = postingList2[i2]
        if p1DocId == p2DocId:
            result.append(p1DocId)
            i1 += 1
            i2 += 1

        elif p1DocId < p2DocId:
            # later can implement skip pointer for p1
            i1 += 1

        else:
            # later can implement skip pointer for p2
            i2 += 1

    return result


def ANDWithTfInFirstList(postingList1, postingList2):
    # print(postingList1)
    # print(postingList2)
    if len(postingList1) == 0 or len(postingList2) == 0:
        return []
    result = []

    i1 = 0
    i2 = 0
    p1Length = len(postingList1)
    p2Length = len(postingList2)
    while i1 < p1Length and i2 < p2Length:
        p1DocId = postingList1[i1][0]
        p2DocId = postingList2[i2]
        if p1DocId == p2DocId:
            result.append(postingList1[i1])
            i1 += 1
            i2 += 1

        elif p1DocId < p2DocId:
            # later can implement skip pointer for p1
            i1 += 1

        else:
            # later can implement skip pointer for p2
            i2 += 1

    return result


def OR(postingList1, postingList2):
    # print(postingList1)
    # print(postingList2)
    if len(postingList1) == 0:
        return postingList2
    elif len(postingList2) == 0:
        return postingList1
    result = []

    i1 = 0
    i2 = 0
    p1Length = len(postingList1)
    p2Length = len(postingList2)
    while i1 < p1Length and i2 < p2Length:
        p1DocId = postingList1[i1]
        p2DocId = postingList2[i2]
        if p1DocId == p2DocId:
            result.append(p1DocId)
            i1 += 1
            i2 += 1

        elif p1DocId < p2DocId:
            result.append(p1DocId)
            i1 += 1

        else:
            result.append(p2DocId)
            i2 += 1

    if i1 < p1Length:
        result += [ tu for tu in postingList1[i1:] ]
    elif i2 < p2Length:
        result += [ tu for tu in postingList2[i2:] ]
    return result


def booleanQuery(query):
    if len(query) == 0:
        return None
    elif len(query) == 1:
        if query[0] in dic:
            return [ x[0] for x in getPostingList(postings_file, dic[query[0]]) ]
        else:
            return None

    # query here must have size larger than 1
    postings = []
    for term in query:
        if term not in dic:
            return None
        else:
            posting = getPostingList(postings_file, dic[term])
            if posting != None:
                # get rid of the second entry of each tuple which is tf
                posting = [x[0] for x in posting]
                postings.append(posting)
            else:
                return None

    result = AND(postings[0], postings[1])
    for p in postings[2:]:
        result = AND(result, p)
    return result

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
        data = f.readline()
        queryResult = None
        
        print("data is: ", data)

        # check if boolean query
        if '"' in data:
            print("boolean query")

            # try free text method
            ###############################################################################
            data = data.replace("AND", ' ')
            data = data.replace('"', ' ')
            # preprocessing
            q = nltk.word_tokenize(data) # now q is a list

            print(q)

            ORIGINAL_NO = len(q)
            print("originally have: ", ORIGINAL_NO)

            # query expansion
            expansion = []
            for word in q:
                expansion += expandOneWord(word)
                # expansion.append(word)
            # print("expansion query words: ", expansion)
            q = expansion

            q = [words.translate(table) for words in q]
            tempQ = []
            for words in q:
                for word in words.split(' '):
                    if len(word) > 0:
                        tempQ.append(word)
            q = [caseFoldigAndStemming(token) for token in tempQ]
            
            # remove strange puntuation
            terms = []
            for word in q:
                if '–' in word or word == '–' or word in stopwords:
                    continue
                else:
                    terms.append(word)
            q = terms


            # remove duplicates
            q = set(q)
            q = list(q)
            print("final q:", q)
            # print("expansion: ", queryExpansion(q))
            # execute query
            queryResult = cosineScore(q, False)
            ###############################################################################




            # # for storing preprocessed queries.
            # # each element is either a phrase (words separated by a space) or word
            # queries = []
            # preprocessResult = []



            # qList = data.replace('AND', ' ')

            # # query expansion
            # expansion = []

            # qList = nltk.word_tokenize(qList)
            # # print(qList)

            # # expansion += q
            # for word in qList:
            #     expansion.append( expandOneWordForBooleanQuery(word) )
            #     # expansion.append(word)

            # qList = expansion

            # # print(qList)

            # # remove puntuation
            # for i in range(len(qList)):
            #     qList[i] = [words.translate(table).strip() for words in qList[i]]

            # # split two words into one
            # for i in range(len(qList)):
            #     tempList = []
            #     for words in qList[i]:
            #         for word in words.split():
            #             tempList.append(word)
            #     qList[i] = tempList

            # # print(qList)
            # tempList = []
            # for lis in qList:
            #     if len(lis) == 0:
            #         continue
            #     tempList.append(lis)

            # qList = tempList
            # # print("removed empty list", qList)

            # tempList = []
            # for lis in qList:
            #     lis = [caseFoldigAndStemming(token) for token in lis]
            #     tempList.append(lis)

            # qList = tempList

            # # print(qList)
            
            # # remove strange puntuation
            # for i in range(len(qList)):
            #     tempList = []
            #     for word in qList[i]:
            #         if '–' in word or word == '–':
            #             continue
            #         else:
            #             tempList.append(word)
            #     qList[i] = tempList

            # # print("should be the same as before")
            # # print(qList)

            # # remove query that are not in dic
            # for i in range(len(qList)):
            #     tempList = []
            #     for word in qList[i]:
            #         if word not in dic:
            #             continue
            #         else:
            #             tempList.append(word)
            #     qList[i] = tempList

            # queries = qList



            # # # remove duplicates
            # # queries = set(queries)
            # # queries = list(queries)
            # # execute query
            # print("final q:", queries)
            # # queryResult = booleanQuery(queries)
            # queryResult = cosineScore(queries, True)

        # if free text query
        else:
            print("free text query")
            # preprocessing
            q = nltk.word_tokenize(data) # now q is a list

            ORIGINAL_NO = len(q)
            print("originally have: ", ORIGINAL_NO)

            # query expansion
            expansion = []
            for word in q:
                expansion += expandOneWord(word)
                # expansion.append(word)
            # print("expansion query words: ", expansion)
            q = expansion

            q = [words.translate(table) for words in q]
            tempQ = []
            for words in q:
                for word in words.split(' '):
                    if len(word) > 0:
                        tempQ.append(word)
            q = [caseFoldigAndStemming(token) for token in tempQ]
            
            # remove strange puntuation
            terms = []
            for word in q:
                if '–' in word or word == '–' or word in stopwords:
                    continue
                else:
                    terms.append(word)
            q = terms


            # remove duplicates
            q = set(q)
            q = list(q)
            print("final q:", q)
            # print("expansion: ", queryExpansion(q))
            # execute query
            queryResult = cosineScore(q, False)

        if queryResult != None:
            print("number of result: ", len(queryResult))

            query_no = int(file_of_output.split('.')[1])

            # evaluate score
            required = []
            # q1
            required.append([6807771, 4001247, 3992148])

            # q2
            required.append([2211154, 2748529])

            # q3
            required.append([4273155, 3243674, 2702938])

            requiredDic = {}

            for i in range(len(queryResult)):
                if queryResult[i] in required[query_no-1]:
                    requiredDic[queryResult[i]] = i

            print(requiredDic)

        if queryResult == None:
            t.write('\n')
        else:
            t.write(' '.join(str(d) for d in queryResult) + '\n')