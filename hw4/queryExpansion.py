#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 00:22:50 2018

@author: weiqing
"""

import nltk
from nltk.corpus.reader.wordnet import NOUN
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer 
    

#termQ = ["word","hello"]

def queryExpansion(self, query):
    termQ = query
    newList =[]
      
    for term in termQ:
    
        wn1 = WordNetLemmatizer()
        
        lol =  (wn1.lemmatize(term))
        
        print(lol)
        
        syns = []
        for syn in  wn.synsets(lol):
            for l in syn.lemmas():
                syns.append(l.name())
        
        setS = set(syns)
        listS = list(setS)
        
        for word in listS:
            if "_" not in word:
                newList.append(word)
            elif "_":
                tk =  word.split("_")
                for term in tk:
                    newList.append(term)
        
    
    #print(newList)
    return newList