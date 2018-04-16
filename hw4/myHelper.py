import nltk
import pickle
import math
import sys
import string


table = str.maketrans({key: ' ' for key in string.punctuation})

## get from string.punctuation
#string_punct = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',',
#                '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\',
#                ']', '^', '_', '`', '{', '|', '}', '~', '--', "''", '...', '–']

# get stemmer from nltk
ps = nltk.stem.PorterStemmer()

# special term for saving all docID
special_term = "ALL_DOC_ID"

def putDocIntoList(lis, docContent, docId):
    tokens = []
    
    # tokenize
    for words in nltk.word_tokenize(docContent):
        words.translate(table)
        for word in words.split(' '):
            tokens.append(word)
        
    tokens = [word for word in nltk.word_tokenize(docContent)]
    initTerms = [caseFoldigAndStemming(token) for token in tokens]
    terms = []
    for term in initTerms:
        if "–" in term or term == '—':
            continue
        else:
            terms.append(term)

    # add unigram into lis
    for term in terms:
        lis.append((term, docId))
    
    # add bigram into lis
    if len(terms) >= 2:
        for i in range(len(terms)-1):
            lis.append((terms[i]+' '+terms[i+1], docId))
    
    # add trigram into lis
    if len(terms) >= 3:
        for i in range(len(terms)-2):
            lis.append((terms[i]+' '+terms[i+1]+' '+terms[i+2], docId))

def average_jumps(length):
    average_jump = int(math.floor(math.sqrt(length)))
    return average_jump

# functions defined by Gordon


def caseFoldigAndStemming(input):
    return ps.stem(input.lower())

# retrieve posting list from file


def getPostingList(filename, dictValue):
    if dictValue == None:
        return None
    if dictValue.getPointer() == None:
        return None
    with open(filename, mode="rb") as f:
        p = dictValue.getPointer()
        f.seek(p[0])
        return pickle.loads(f.read(p[1]))

# print posting list for debugging


def printPostingList(postingList):
    if postingList == None:
        print("Posting list has nothing")
        return None
    h = postingList.getHead()
    count = 0
    ids = []
    while h != None:
        count += 1
        ids.append(h.getDocId())
        h = h.getNext()
    print(" ".join(str(x) for x in ids))
    print("frequency:", count)


def printSkipPointerList(postingList):
    h = postingList.getHead()
    count = 0
    while h != None:
        count += 1
        print(h.getDocId())
        h = h.getSkipNext()
    print("frequency:", count)


def writePostingListToFile(file, postingList):
    if postingList == None:
        file.write("\n")
        return None
    h = postingList.getHead()
    ids = []
    while h != None:
        ids.append(h.getDocId())
        h = h.getNext()
    file.write(" ".join(str(x) for x in ids) + "\n")


# classes created by Gordon


class Node:
    """Posting list node"""

    def __init__(self, docId):
        self.docId = docId
        self.next = None
        self.skipNext = None
        self.termFrequency = 1

    def getDocId(self):
        return self.docId

    def getNext(self):
        return self.next

    def getSkipNext(self):
        return self.skipNext

    def getTermFrequency(self):
        return self.termFrequency

    def setNext(self, node):
        self.next = node

    def setSkipNext(self, node):
        self.skipNext = node

    def incrementTermFrequency(self):
        self.termFrequency = self.termFrequency + 1

    def calculateLogTF(self):
        self.termFrequency = 1 + math.log(self.termFrequency, 10)


class PostingList:

    def __init__(self, head):
        self.head = head
        self.currentNode = head
        self.frequency = 1

    def add(self, node):
        """add all nodes into the list first before calling resetCurrentNode"""
        self.currentNode.setNext(node)
        self.currentNode = node
        self.frequency += 1

    def resetCurrentNode(self):
        self.currentNode = self.head

    def getHead(self):
        return self.head

    def getFrequency(self):
        return self.frequency

    def getCurrentNode(self):
        return self.currentNode


class DicValue:
    """DicValue class with attribute frequency and pointer to posting list
    Pointer is a tuple with two integer value. It indicate the location of the
    posting list stored in postings.txt file. The first value is the byte
    offset of the corresponding posting list stored in the postings.txt file.
    The second is the length of it. Note that it is the bytes encoded by pickle.
    """

    def __init__(self, postingList):
        self.docF = 1
        self.pL = postingList
        self.pointer = None

    def getPostingList(self):
        return self.pL

    def getDocFrequency(self):
        return self.docF

    def getPointer(self):
        return self.pointer

    def addOneDoc(self):
        self.docF += 1

    def setPostingList(self, pL):
        self.pL = pL

    def setPointer(self, pointer):
        self.pointer = pointer

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "({}, {}, {})".format(self.term, self.docF, self.pL)
