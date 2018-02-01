#!/usr/bin/python
import re
import nltk
import sys
import getopt

import string
import pprint
pp = pprint.PrettyPrinter(indent=4)

#translator = str.maketrans('', '', string.punctuation+'°'+'1234567890')

def preprocess_line(line):
    # removing newline character and convert all character to lower case
    line = line.replace('\n', '').lower()
    
    # split the label and the text
    return line.split(maxsplit=1)

def convert_line_to_4gramList(line):
    if len(line) >= 4:
        return [ line[i:i+4] for i in range(len(line)-3) ]
    else:
        sys.exit("Cannot produce 4-gram with less than 4 characters")

def convert_counts_to_probability(number, lm):
    total_words = len(lm)
    for gram in lm:
        for lang in lm[gram]:
            count = lm[gram][lang]
            lm[gram][lang] = count/(number[lang] + total_words)
    return lm

"""
 return my language model
 each key is defined to be a 4-grams in our training text
 each value is defined to be a dictionary with keys being each language
 and values being the frequency of the 4-grams appearing in that language in
 our training text"""
def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and a string separated by a space
    """
    print('building language models...')
    # This is an empty method
    # Pls implement your code in below
    
    LM = {}
    
    # counting total number of 4-grams in each language in the training text
    total_no_of_words = {"malaysian":0, "indonesian":0, "tamil":0}
    
    with open(in_file, mode="r", encoding="utf-8") as f:
        textList = f.readlines()
        
        # striping out the numbers and punctuation
#        for i in range(len(textList)):
#            textList[i] = textList[i].translate(translator).replace('\n', '').lower()
        
        for line in textList:
            
            [label, text] = preprocess_line( line )
#            pp.pprint([label, text])
            
            # count the number of 4-grams for each line in training text
            if len(text) >= 4 and label in total_no_of_words:
                total_no_of_words[label] += len(text) - 3
            else:
                sys.exit("Error! Some sentences in the training text contains "
                      "less than 4 characters!!! OR the language is not "
                      "malasian, indonesian, or tamil.")
            
            grams = convert_line_to_4gramList(text)
            
            # update the count for each gram in our language model
            for gram in grams:
                
                # init to be zero
                if gram not in LM:
                    LM[gram] = {"malaysian":0, "indonesian":0, "tamil":0}
                
                # update count
                LM[gram][label] += 1
        
        
        print(LM['tra '])
        
        # add one smoothing for each gram
        for gram in LM:
            for lang in LM[gram]:
                LM[gram][lang] += 1
        
        print(LM['tra '])
        
        return convert_counts_to_probability(total_no_of_words, LM)
    
def test_LM(in_file, out_file, LM):
    """
    test the language models on new strings
    each line of in_file contains a string
    you should print the most probable label for each string into out_file
    """
    print("testing language models...")
    # This is an empty method
    # Pls implement your code in below

def usage():
    print("usage: " + sys.argv[0] +
          " -b input-file-for-building-LM "
          "-t input-file-for-testing-LM "
          "-o output-file")

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except getopt.GetoptError as err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
