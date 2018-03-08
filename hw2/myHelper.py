import nltk
import pickle

# get from string.punctuation
string_punct = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

# get stemmer from nltk
ps = nltk.stem.PorterStemmer()

# special term for saving all docID
special_term = "ALL_DOC_ID"

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
    while h != None:
        count += 1
        print(h.getDocId())
        h = h.getNext()
    print("frequency:", count)


def printSkipPointerList(postingList):
    h = postingList.getHead()
    count = 0
    while h != None:
        count += 1
        print(h.getDocId())
        h = h.getSkipNext()
    print("frequency:", count)
# classes created by Gordon


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
