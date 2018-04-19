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


def cosineScore(q):
    """
    q is a list of string where each string is a unigram"""

    # compute weighted tf_t,q
    queryDic = calculateQueryLogTF(q)
    queryDic = multiplyIDF(queryDic)

    # nothing to query
    if queryDic == None:
        return None

    # init scores for every doc
    scores = [[i, None] for i in range(len(docIds))]

    # compute dot product
    for term in queryDic:
        # load posting list
        # term must be in dic
        # otherwise it is removed in calculateQueryLogTF function
        pl = getPostingList(postings_file, dic[term])
        
        for tempDocId, w_tf in pl:
            # retrieve the corresponding index in scores array
            indexInScores = docIdToIndexMap[tempDocId]
#            print(indexInScores, term, tempDocId, h.getTermFrequency(), queryDic[term])

            if scores[indexInScores][1] == None:
                scores[indexInScores][1] = w_tf * queryDic[term]
            else:
                scores[indexInScores][1] += w_tf * queryDic[term]

    # normalize scorse by the corresponding weighted doc vector length
    for x in scores:
        if x[1] != None:
            x[1] /= lengthOfDocument[ docIds[x[0]] ][1]

    # compute a list of tuple consisting of a nonNone-score docId and its score
    nonzeroScoresList = [(x[0], x[1]) for x in scores if x[1] != None]
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
    print(postingList1)
    print(postingList2)
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


def booleanQuery(query):
    if len(query) == 0:
        return None
    elif len(query) == 1:
        if query[0] in dic:
            return getPostingList(postings_file, dic[query[0]])
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
                postings.append(posting)
            else:
                return None
    
    # get rid of the second entry of each tuple which is tf
    for i in range(len(postings)):
        postings[i] = [x[0] for x in postings[i]]

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
        if '"' in data or 'AND' in data:

            # for storing preprocessed queries.
            # each element is either a phrase (words separated by a space) or word
            queries = []
            preprocessResult = []
            if 'AND' in data:
                qList = data.split('AND')

                # preprocessing
                for q in qList:
                    q = q.replace('"', '')
                    q = nltk.word_tokenize(q)
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
                    preprocessResult.append(terms)

                # join back the processed term for phrase query
                for q in preprocessResult:
                    if len(q) <= 3:
                        queries.append(' '.join(q))
                    else:
                        for i in range(len(q) - 2):
                            queries.append(' '.join(q[i:i + 3]))
            else:
                q = data
                q = q.replace('"', '')
                q = nltk.word_tokenize(q) # now q is a list
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

                # join back the processed term for phrase query
                if len(q) <= 3:
                    queries.append(' '.join(q))
                else:
                    for i in range(len(q) - 2):
                        queries.append(' '.join(q[i:i + 3]))

            # execute query
#            print(queries)
            queryResult = booleanQuery(queries)
            writePostingListToFile(t, queryResult)
            print(queryResult)

        # if free text query
        else:

            # preprocessing
            q = nltk.word_tokenize(data) # now q is a list
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

#            print(q)
            # execute query
            queryResult = cosineScore(q)
            if queryResult == None:
                t.write('\n')
            else:
                t.write(' '.join(str(d) for d in queryResult) + '\n')