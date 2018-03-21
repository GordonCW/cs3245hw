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
"""
Hi Wei Qing,

implement the Shunting-yard algorithm here

"""
from nltk.tokenize import sent_tokenize, word_tokenize


def shunting_yard_algo(lst):

    # do "not" first, then "and" , then "or"

    operator = {"OR": 0, "AND": 1, "NOT": 2, "(": -1, ")": -1}
    postfix = []
    opt_stack = []
    lst = word_tokenize(lst)

    for token in lst:
        if token in operator:
            if token == "(":
                opt_stack.append(token)
            elif token == ")":
                while len(opt_stack) > 0:
                    top_token = opt_stack.pop()
                    if (top_token == "("):
                        break
                    else:
                        postfix.append(top_token)
            # not a parenthesis

            else:
                if len(opt_stack) == 0:
                    opt_stack.append(token)

                else:
                    # check the ranking
                    while len(opt_stack) > 0 and \
                            operator[opt_stack[-1]] > operator[token]:
                        addOperator = opt_stack.pop()
                        postfix.append(addOperator)

                    opt_stack.append(token)
        else:
            postfix.append(token)
    while len(opt_stack) > 0:
        operator_leftover = opt_stack.pop()
        postfix.append(operator_leftover)

    return postfix

# https://en.wikipedia.org/wiki/Reverse_Polish_notation


def postfixEvaluation(postfix):

    stack = []
    operator = []
    operator.append("OR")
    operator.append("AND")
    operator.append("NOT")

    while len(postfix) >= 1:
        # get the first item
        token = postfix.pop(0)

        if token in operator:
            result = None
            if token == "OR":
                operand1 = stack.pop()
                operand2 = stack.pop()
                result = OR(operand1, operand2)
            elif token == "AND":

                i = 0
                # count the number of consecutive "AND"
                for expression in postfix:
                    if expression != "AND":
                        break
                    i += 1

                # remove the counted ones
                for j in range(i):
                    postfix.pop(0)

                # total number of consecutive "AND"s = i + 1

                # merging the shortest list first
                if (i + 1) >= 2:

                    # find the shortest list length
                    minLength = stack[-1].getFrequency()
                    for j in range(i + 2):
                        if minLength > stack[-1 - j].getFrequency():
                            minLength = stack[-1 - j].getFrequency()

                    # get the shortest posting list and a list of remaining lists
                    postingListContainer = []
                    for j in range(i + 2):
                        tempPostingList = stack.pop()
                        postingListContainer.append(tempPostingList)

                    operand1 = None
                    for j in range(len(postingListContainer)):
                        if minLength == postingListContainer[j].getFrequency():
                            operand1 = postingListContainer[j]
                            postingListContainer.pop(j)
                            break

                    # do the merging
                    for postingList in postingListContainer:
                        operand1 = AND(operand1, postingList)

                    # put the result in the result variable
                    result = operand1

                # usual merge
                else:
                    operand1 = stack.pop()
                    operand2 = stack.pop()
                    result = AND(operand1, operand2)

            else:
                if token == "NOT":
                    token1 = postfix.pop(0)
                    if token1 == "AND":
                        operand1 = stack.pop()
                        operand2 = stack.pop()
                        result = ANDNOT(operand2, operand1)
                    elif token1 not in operator and postfix[0] == "AND":
                        # get rid of AND
                        postfix.pop(0)

                        # the Z
                        token1 = caseFoldigAndStemming(token1)
                        chosen1 = getPostingList(postings_file, dic[token1])
                        chosen2 = stack.pop()

                        result = ANDNOT(chosen1, chosen2)
                    else:
                        postfix.insert(0, token1)
                        operand1 = stack.pop()
                        result = NOT(operand1)
            stack.append(result)
        else:
            token = caseFoldigAndStemming(token)
            if token in dic:
                stack.append(getPostingList(postings_file, dic[token]))

            else:
                stack.append(None)

    finalResult = stack.pop()
    return finalResult


# functions defined by Gordon

def AND(postingList1, postingList2):
    if postingList1 == None or postingList2 == None:
        return None
    result = None
    p1 = postingList1.getHead()
    p2 = postingList2.getHead()
    while p1 != None and p2 != None:
        if p1.getDocId() == p2.getDocId():

            if result == None:
                result = PostingList(Node(p1.getDocId()))
            else:
                result.add(Node(p1.getDocId()))
            p1 = p1.getNext()
            p2 = p2.getNext()

        elif p1.getDocId() < p2.getDocId():

            if p1.getSkipNext() != None:
                tempP = p1.getSkipNext()

                # use skip pointer if the order is preserved
                if tempP.getDocId() <= p2.getDocId():
                    p1 = tempP
                else:
                    p1 = p1.getNext()
            else:
                p1 = p1.getNext()

        else:

            if p2.getSkipNext() != None:
                tempP = p2.getSkipNext()

                # use skip pointer if the order is preserved
                if tempP.getDocId() <= p1.getDocId():
                    p2 = tempP
                else:
                    p2 = p2.getNext()
            else:
                p2 = p2.getNext()

    return result


def ANDNOT(postingList1, postingList2):
    """NOT the sencond posting list"""
    if postingList1 == None:
        return None
    if postingList2 == None:
        return postingList1
    result = None
    p1 = postingList1.getHead()
    p2 = postingList2.getHead()
    while p1 != None and p2 != None:
        if p1.getDocId() == p2.getDocId():

            p1 = p1.getNext()
            p2 = p2.getNext()

        elif p1.getDocId() < p2.getDocId():

            # save p1's id before going to the next one
            if result == None:
                result = PostingList(Node(p1.getDocId()))
            else:
                result.add(Node(p1.getDocId()))
            p1 = p1.getNext()

        else:

            p2 = p2.getNext()

    if p1 != None:
        result.add(p1)

    return result


def OR(postingList1, postingList2):
    if postingList1 == None:
        return postingList2
    if postingList2 == None:
        return postingList1
    result = None
    p1 = postingList1.getHead()
    p2 = postingList2.getHead()
    while p1 != None and p2 != None:
        if p1.getDocId() == p2.getDocId():

            if result == None:
                result = PostingList(Node(p1.getDocId()))
            else:
                result.add(Node(p1.getDocId()))
            p1 = p1.getNext()
            p2 = p2.getNext()

        elif p1.getDocId() < p2.getDocId():

            if result == None:
                result = PostingList(Node(p1.getDocId()))
            else:
                result.add(Node(p1.getDocId()))
            p1 = p1.getNext()

        else:

            if result == None:
                result = PostingList(Node(p2.getDocId()))
            else:
                result.add(Node(p2.getDocId()))
            p2 = p2.getNext()
    if p1 != None:
        result.add(p1)
    elif p2 != None:
        result.add(p2)
    return result


def NOT(postingList):
    wholeDocIdList = getPostingList(postings_file, dic[special_term])
    if postingList == None:
        return wholeDocIdList
    result = None
    p1 = wholeDocIdList.getHead()
    p2 = postingList.getHead()
    while p1 != None and p2 != None:
        if p1.getDocId() == p2.getDocId():

            p1 = p1.getNext()
            p2 = p2.getNext()

        elif p1.getDocId() < p2.getDocId():

            if result == None:
                result = PostingList(Node(p1.getDocId()))
            else:
                result.add(Node(p1.getDocId()))
            p1 = p1.getNext()

        else:

            sys.exit("Not operation error!!!!!!")

    if p1 != None:
        result.add(p1)

    return result

def calculateQueryLogTF(q):
    tempList = []
    tempQueryDic = {}
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
        tempQueryDic[term] *= math.log(N/dic[term].getDocFrequency(), 10)
    
    return tempQueryDic

def cosineScore(q):
    # init scores
    scores = [ [i, 0] for i in range(len(docIds))]
    
    # compute weighted tf_t,q
    queryDic = calculateQueryLogTF(q)
    queryDic = multiplyIDF(queryDic)
    
    # nothing to query
    if queryDic == None:
        return None
    
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
            
            # accumulate scores
            # h.getTermFrequency() return the weighted tf as computed in index.py
            scores[indexInScores][1] += h.getTermFrequency() * queryDic[term]
            
            h = h.getNext()
    
    # compute a list of tuple consisting of a nonzero-score docId and its score
    nonzeroScoresList = [(x[0], x[1]) for x in scores if x[1]>0]
    
    result = None
    if len(nonzeroScoresList) > 10:
        result = heapq.nlargest(10, nonzeroScoresList, key=lambda x: x[1])
    else:
        result = nonzeroScoresList.sort(key=lambda x: x[1], reverse=True)

    # return the real docIds
    return [docIds[x[0]] for x in result]

# code start here


# load dic back into memory
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

#pl = getPostingList(postings_file, dic['year'])
#h = pl.getHead()
#while h != None:
#    print(h.getDocId(), end=' ')
#    h = h.getNext()
#print()

# read queries and process it
# write it back to the result file
with open(file_of_output, "w", encoding="utf-8") as t:
    with open(file_of_queries, "r", encoding="utf-8") as f:
        data = f.readlines()
        for query in data:
            query = query.rstrip("\n")
            query = word_tokenize(query)
            query = [caseFoldigAndStemming(token) for token in query]
            queryResult = cosineScore(query)
            if queryResult == None:
                t.write('\n')
            else:
                t.write(' '.join(str(x) for x in queryResult) + '\n')
            
