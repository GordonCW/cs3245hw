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
from nltk.tokenize import sent_tokenize, word_tokenize


def shunting_yard_algo(lst):

    # do "not" first, then "and" , then "or"

     operator = {"OR": 0, "AND": 1, "NOT": 2, "(": -1, ")": -1}
     postfix = []
     opt_stack = []
     lst = word_tokenize(lst)

     for token in lst:
        if token in operator:
            if token =="(":
                opt_stack.append(token)
            elif token == ")":
                while len(opt_stack) > 0:
                    top_token = opt_stack.pop()
                    if (top_token == "("):
                        break
                    else:
                        postfix.append(top_token)
            #not a parenthesis
            
            else:
                print(token)
                if len(opt_stack) == 0:
                    opt_stack.append(token)

                else:
                    #check the ranking
                    while  len(opt_stack) > 0 and \
                    operator[opt_stack[-1]] > operator[token]:
                           addOperator = opt_stack.pop()
                           postfix.append(addOperator)
                    
                    opt_stack.append(token)
        else:
             postfix.append(token)
     while len(opt_stack) >  0:
         operator_leftover = opt_stack.pop()
         postfix.append( operator_leftover )

     return postfix

#https://en.wikipedia.org/wiki/Reverse_Polish_notation
def postfixEvaluation(postfix):
    
    stack = []
    operator = []
    operator.append("OR")
    operator.append("AND")
    operator.append("NOT")

    while len(postfix) >= 1:
        #get the first item
        token = postfix.pop(0)
        
        if token in operator:
            result = None
            if token == "OR":
                operand1 = stack.pop()
                operand2 = stack.pop()
                result = OR(operand1, operand2)
#                print("used OR!!!!!")
#                print("below is the result of OR")
#                printPostingList(result)
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
                    minLength = stack[ -1 ].getFrequency()
                    for j in range(i + 2):
                        if minLength > stack[ -1 - j ].getFrequency():
                            minLength = stack[ -1 - j ].getFrequency()
                    
                    # get the shortest posting list and a list of remaining lists
                    postingListContainer = []
                    for j in range(i + 2):
                        tempPostingList = stack.pop()
                        postingListContainer.append( tempPostingList )
                    
                    operand1 = None
                    for j in range( len(postingListContainer) ):
                        if minLength == postingListContainer[j].getFrequency():
                            operand1 = postingListContainer[j]
                            postingListContainer.pop(j)
                            break
                    
#                    print(len(postingListContainer))
#                    print("see posting list hereeeeeeeee")
#                    printPostingList(operand1)
                    # do the merging
                    for postingList in postingListContainer:
                        printPostingList(postingList)
                        operand1 = AND(operand1, postingList)
                    
                    # put the result in the result variable
                    result = operand1
                
                # usual merge
                else:
                    operand1 = stack.pop()
                    operand2 = stack.pop()
                    result = AND(operand1, operand2)
                    
#                print("used AND!!!!!")
#                print("below is the result of AND")
#                printPostingList(result)
            else:
                if token == "NOT":
                    token1 = postfix.pop(0)
                    if  token1 == "AND":
                        operand1 = stack.pop()
                        operand2 = stack.pop()
                        result = ANDNOT(operand2, operand1)
#                        print("used ANDNOT!!!!!")
#                        print("below is the result of ANDNOT")
#                        printPostingList(result)
                    elif token1 not in operator and postfix[0] == "AND":
                        #get rid of AND
                        postfix.pop(0)
                        
                        #the Z
                        token1 = caseFoldigAndStemming(token1)
                        chosen1 = getPostingList(postings_file, dic[token1])
                        chosen2 = stack.pop()
                        
#                        print()
#                        print(token1)
#                        printPostingList(chosen1)
#                        print()
#                        printPostingList(chosen2)
                        
                        result = ANDNOT(chosen1, chosen2)
#                        print("used ANDNOT!!!!!")
#                        print("below is the result of ANDNOT")
#                        printPostingList(result)
                    else:
                        postfix.insert(0, token1)
                        operand1 = stack.pop()
                        result = NOT(operand1)
#                        print("used NOT!!!!!")
#                        print("below is the result of NOT")
#                        printPostingList(result)
            stack.append(result) 
        else:
            token = caseFoldigAndStemming(token)
            if token in dic:
#                print("This token is")
#                print(token)
                stack.append( getPostingList(postings_file, dic[token]) )
                
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
                result = PostingList( Node(p1.getDocId()) )
            else:
                result.add( Node(p1.getDocId()) )
            p1 = p1.getNext()
            p2 = p2.getNext()
            
        elif p1.getDocId() < p2.getDocId():
            
            if p1.getSkipNext() != None:
                tempP = p1.getSkipNext()
                
                # use skip pointer if the order is preserved
                if tempP.getDocId() <= p2.getDocId():
                    p1 = tempP
                    print("skip pointer used")
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
                    print("skip pointer used")
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
                result = PostingList( Node(p1.getDocId()) )
            else:
                result.add( Node(p1.getDocId()) )
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
                result = PostingList( Node(p1.getDocId()) )
            else:
                result.add( Node(p1.getDocId()) )
            p1 = p1.getNext()
            p2 = p2.getNext()
            
        elif p1.getDocId() < p2.getDocId():
            
            if result == None:
                result = PostingList( Node(p1.getDocId()) )
            else:
                result.add( Node(p1.getDocId()) )
            p1 = p1.getNext()
            
        else:
            
            if result == None:
                result = PostingList( Node(p2.getDocId()) )
            else:
                result.add( Node(p2.getDocId()) )
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
                result = PostingList( Node(p1.getDocId()) )
            else:
                result.add( Node(p1.getDocId()) )
            p1 = p1.getNext()
            
        else:
            
            sys.exit("Not operation error!!!!!!")
            
    if p1 != None:
        result.add(p1)
        
    return result



######### code start here

# load dic back into memory
dic = None
with open(dictionary_file, mode="rb") as f:
    dic = pickle.load(f)
    
    
######### test case here
# mainly test skip pointer here
print("Posting List of \"the\"")
p1 = getPostingList(postings_file, dic["the"])
printPostingList( p1 )

print()

print("Posting List of \"show\"")
p2 = getPostingList(postings_file, dic["show"])
printPostingList( p2 )

print()

print("Posting List of the AND show")
resu = AND(p1, p2)
printPostingList( resu )


print()
print()
print()


# mainly test correctness AND here
print("Posting List of \"approv\"")
p1 = getPostingList(postings_file, dic["approv"])
printPostingList( p1 )

print()

print("Posting List of \"show\"")
p2 = getPostingList(postings_file, dic["show"])
printPostingList( p2 )

print()

print("Posting List of approv AND show")
resu = AND(p1, p2)
printPostingList( resu )

print()
print()
print()

# mainly test correctness of OR here
print("Posting List of \"pay\"")
p1 = getPostingList(postings_file, dic["pay"])
printPostingList( p1 )

print()

print("Posting List of \"show\"")
p2 = getPostingList(postings_file, dic["show"])
printPostingList( p2 )

print()

print("Posting List of pay OR show")
resu = OR(p1, p2)
printPostingList( resu )

print()
print()
print()

# mainly test correctness ANDNOT here
print("Posting List of \"approv\"")
p1 = getPostingList(postings_file, dic["approv"])
printPostingList( p1 )

print()

print("Posting List of \"show\"")
p2 = getPostingList(postings_file, dic["show"])
printPostingList( p2 )

print()

print("Posting List of approv ANDNOT show")
resu = ANDNOT(p1, p2)
printPostingList( resu )


print()
print()
print()

# mainly test correctness OR here
print("Posting List of \"approv\"")
p1 = getPostingList(postings_file, dic["approv"])
printPostingList( p1 )

print()

print("Posting List of \"show\"")
p2 = getPostingList(postings_file, dic["show"])
printPostingList( p2 )

print()

print("Posting List of approv OR show")
resu = OR(p1, p2)
printPostingList( resu )


print()
print()
print()


# mainly test correctness NOT here
print("Posting List of \"and\"")
p1 = getPostingList(postings_file, dic["approv"])
printPostingList( p1 )

print()

print("Posting List of NOT and")
resu = NOT(p1)
printPostingList( resu )
print(dic[special_term].getDocFrequency())


print()
print()
print()

# read queries and process it
# write it back to the result file
with open(file_of_output, "w", encoding="utf-8" ) as t:
    with open(file_of_queries, "r",  encoding="utf-8" ) as f:
        data = f.readlines()
        print(data)
        for query in data:
            query = query.rstrip("\n")
            print(query)
            
            post_fix = shunting_yard_algo(query)
            print(post_fix)
            
            ans = postfixEvaluation(post_fix)
            
            print()
            print()
            print()
            print("result of the query::::::::::")
            printPostingList(ans)
            print()
            print()
            print()
            writePostingListToFile(t, ans)


p1 = getPostingList(postings_file, dic["will"])
p2 = getPostingList(postings_file, dic["vs"])

print("Posting List of NOT and")
resu = AND(p1, p2)
p3 = getPostingList(postings_file, dic["trade"])
resu = AND(resu, p3)
p3 = getPostingList(postings_file, dic["they"])
resu = ANDNOT(resu, p3)



p3 = getPostingList(postings_file, dic["than"])
resu = AND(resu, p3)

p3 = getPostingList(postings_file, dic["stock"])
resu = OR(resu, p3)
printPostingList( resu )




