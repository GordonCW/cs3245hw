#!/usr/bin/python
import re
import nltk
import sys
import getopt

# get from string.punctuation
string_punct = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

# get stemmer from nltk
ps = nltk.stem.PorterStemmer()

def usage():
    print("usage: " + sys.argv[0] +\
          " -i directory-of-documents -d dictionary-file -p postings-file")

input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError as err:
    usage()
    sys.exit(2)
    
for o, a in opts:
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"
        
if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

"""
start my code here
"""

######### functions defined by Gordon

def caseFoldigAndStemming(input):
    return ps.stem(input.lower())

######### classes created by Gordon

class Node:
    """Posting list node"""
    
    def __init__(self, docId):
        self.docId = docId
        self.next = None
        self.skipNext = None
        
    def getDocId(self):
        return self.docId
        
    def getNext(self):
        return self.next
    
    def getSkipNext(self):
        return self.skipNext
    
    def setNext(self, node):
        self.next = node
        
    def setSkipNext(self, node):
        self.skipNext = node

class PostingList:
    
    def __init__(self, head):
        self.head = head
        self.currentNode = head
        
    def add(self, node):
        """add all nodes into the list first before calling resetCurrentNode"""
        self.currentNode.setNext(node)
        self.currentNode = node
        
    def resetCurrentNode(self):
        self.currentNode = self.head
        
    def getHead(self):
        return self.head

class DicValue:
    """DicValue class with attribute frequency and pointer to posting list
    """
    
    def __init__(self, postingList):
        self.docF = 1
        self.pL = postingList
    
    def addOneDoc(self):
        self.docF += 1

    def getPostingList(self):
        return self.pL
    
    def getDocFrequency(self):
        return self.docF

    def setpLHead(self, pL):
        self.pLHead = pL
        
    def __repr__(self):
        return str(self)
        
    def __str__(self):
        return "({}, {}, {})".format(self.term, self.docF, self.pL)

######### code start here

# get file name from the input directory
# sort file name by number
from os import listdir
from os.path import isfile, join
files = [f for f in listdir(input_directory) if isfile(join(input_directory, f))]
files.sort(key=int)
print(files)

# save tuples
dictionary = []

# save DictElement
dic = {}
for file in files[:6]:
    
    with open(input_directory + '/' + file, mode="r", encoding="utf-8") as f:
        textList = f.readlines()
    
    for line in textList:
        for word in nltk.word_tokenize(line):
            if word not in string_punct:   # to get rid of single punctuation
                # make tuple for sorting
                dictionary.append( (caseFoldigAndStemming(word), int(file)) )

# sort by term
dictionary.sort(key=lambda x: x[0])
print(dictionary)

preTuple = None
for tup in dictionary:
    
    # remove duplication
    if tup != preTuple:
        
        # save the term and the docId in dic's value
        if tup[0] not in dic:
            dic[tup[0]] = DicValue( PostingList(Node(tup[1])) )
        else:
            dic[tup[0]].getPostingList().add(Node(tup[1]))
            dic[tup[0]].addOneDoc()
            
        preTuple = tup

"""
Hi Wei Qing,

Add skip pointer code here

"dic" is our final dictionary
the key is the term
the value is the DicValue object
dic[key].getDocFrequency() can get docFrequency
"""

## checking of posting list
#for key in dic:
#    l = dic[key].getPostingList()
#    l.resetCurrentNode()
#    h = l.getHead()
#    
#    print('count in dic value: ', dic[key].getDocFrequency())
#    count = 0
#    
#    while h != None:
#        count += 1
##        print(h.getDocId())
#        h = h.getNext()
#
#    print("real count in pl: ", count)

# tokenizing
# case-folding
# stemming

# sorting by terms

# count frequency and make posting list

# add skip pointers in posting list

# save posting list in a txt file by pickle
# save dictionary in a txt file