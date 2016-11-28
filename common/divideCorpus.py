# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 13:09:59 2014

@author: varsha
"""
import nltk
import corporaRead as cr
from sets import Set

folds = [];
folds.append([]);
folds.append([]);
folds.append([]);
labels = [];

cr.init("../corpora/Our_corpora/wardrobe_corpus/wardrobe_new_format.txt");

for obj in cr.get_corpora_objects():
        tmp = obj.getLabels();
        tmp.sort();
        labels.append(tmp);

#print labels
unique_labels = [list(x) for x in set(tuple(x) for x in labels)]
#print unique_labels
count = 0;
for tags in unique_labels:
    sentList =  cr.get_corpus_subset_intersect(tags)    
    noSent = len(sentList)
    
    index = 0;
    for obj in sentList:
        snt = obj.getSentences();
        print snt;
        if(index < 3):
            folds[index].append(obj)
            index += 1;
        else:
            index = 0;
            folds[index].append(obj)
            index += 1;
            
index = 0;
for subList in folds:
    if(index == 0):
        f = open('../corpora/Our_corpora/wardrobe_corpus/split_corpora/one.txt', 'wb');
    elif(index == 1):
        f = open('../corpora/Our_corpora/wardrobe_corpus/split_corpora/two.txt', 'wb');
    elif(index == 2):
        f = open('../corpora/Our_corpora/wardrobe_corpus/split_corpora/three.txt', 'wb');
    
    for sentences in subList:
        snt = sentences.getSentences();
        lbl = sentences.getLabels();
        
        sent = ''
        for lbl_trm in lbl:
            sent += '/' + lbl_trm
        sent = sent[1:]
        sent += " -" + snt
        print sent
        f.write(sent);        
        f.write('\n');
#        print sent
        
    index += 1;


   
    
