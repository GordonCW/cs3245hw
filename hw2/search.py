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
            
            p1 = p1.getNext()
            
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
    
    
    
    

## print the posting list of to 
#print('posting list of \"and\" with frequency', dic['and'].getDocFrequency())
#printPostingList( getPostingList(postings_file, dic['and']) )
#
## print the posting list of of
#print('posting list of \"show\" with frequency', dic['show'].getDocFrequency())
#printPostingList( getPostingList(postings_file, dic['show']) )
#
#resu = ANDNOT(getPostingList(postings_file, dic['and']), getPostingList(postings_file, dic['show']))
#
#if resu == None:
#    print("resu is none")
#    
#printPostingList( resu )
#
#print('Not operation of \"and\"')
#printPostingList( NOT(getPostingList(postings_file, dic['and'])) )

    
"""
Hi Wei Qing,

1. load query here
2. execute query in the order that is calculated by the algo
3. save result
"""













