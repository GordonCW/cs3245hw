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

def queryExpansion(query):
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

def expandOneWord(qWord):
    result = []
    # partOfSpeech = ['a', 'n', 'v']
    partOfSpeech = ['n']

    # remove adj
    if wn.morphy(qWord, 'a') != None:
        return [qWord]
                    

    # for pos in partOfSpeech:
    #     # find syn with pos
    #     synL = wn.synsets(qWord, pos)
    #     if len(synL) > 1:
    #         synL = synL[:1]
    #     counter = 0
    #     for syn in synL:
    #         for word in syn.lemmas():
    #             if '_' not in word.name():
    #                 wordName = word.name().lower()
    #                 if wn.morphy(qWord, pos) == wordName:
    #                     continue
    #                 result.append(wordName)
    #                 counter += 1
    #                 if counter == 1:
    #                     break

    # remove dulplicates
    result = set(result)
    result = list(result)
    # print("qWord:", qWord)
    # print(result, '\n')
    # add the origin query word
    result.append(qWord)
    # print("used query expansion")
    return result


def expandOneWordForBooleanQuery(qWord):
    result = []
    # partOfSpeech = ['a', 'n', 'v']
    partOfSpeech = ['n']

    # don't expand adj and verb
    # if wn.morphy(qWord, 'a') != None:
    #     return [qWord]
    # if wn.morphy(qWord, 'v') != None:
    #     return [qWord]
                    

    for pos in partOfSpeech:
        # find syn with pos
        synL = wn.synsets(qWord, pos)
        if len(synL) > 1:
            synL = synL[:1]
        counter = 0
        for syn in synL:
            for word in syn.lemmas():
                if '_' not in word.name():
                    wordName = word.name().lower()
                    if wn.morphy(qWord, pos) == wordName:
                        continue
                    result.append(wordName)
                    counter += 1
                    if counter == 2:
                        break

    result.append(qWord)
    # remove dulplicates
    result = set(result)
    result = list(result)

    return result