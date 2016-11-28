# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 14:11:40 2014

@author: haseeb
"""
import re;
from sets import Set;

from corporaRead import corpusDetail;

sentLabelList = [];

def init(corpora_file):
    
    if len(sentLabelList) != 0:
        return;
        
    f = open(corpora_file,'r');
    labelSentList = [];

    for line in f:
        corpusObject = corpusDetail();
        cleanedline = line.strip()
        if(cleanedline):
            labelSentList = re.split('-',cleanedline)
            tmpList = re.split('/',labelSentList[0]);
            labelList = [];
            for q in tmpList:
                labelList.append(q.strip());
            
            corpusObject.setLabels(labelList);
            
            corpusObject.setSentences(labelSentList[1]); 
            sentLabelList.append(corpusObject);
            
            
def get_corpus_as_list():
    return sentLabelList;

def get_corpus_subset(tags_list):
    """
    usage: corporaRead.get_corpus_subset(["sunny", "hot"])
    return a subset of the corpus with the tags specified in tags_list
    Note! the returned list contains only the sentences themselves, not the tags  
    """
    corpus_subset = Set([]);
    for tag in tags_list:
        for corpush_obj in sentLabelList:
            if tag in corpush_obj.getLabels():
                corpus_subset.add(corpush_obj.getSentences());
    return corpus_subset;
    
def get_corpus_subset_union(tags_list):
    """
    usage: corporaRead.get_corpus_subset_union(["sunny", "hot"])
    return a subset of the corpus; union of all sentences that has one of the tags specified in tags_list
    """
    corpus_subset = Set([]);
    for tag in tags_list:
        for corpush_obj in sentLabelList:
            if tag in corpush_obj.getLabels():
                corpus_subset.add(corpush_obj);
    return corpus_subset;
        
def get_corpus_subset_intersect(tags_list):
    """
    usage: corporaRead.get_corpus_subset_intersect(["sunny", "hot"])
    return a subset of the corpus; intersect of all sentences that has one of the tags specified in tags_list
    """
    corpus_subset = Set([]);
    for corpush_obj in sentLabelList:
        if set(tags_list) == set(corpush_obj.getLabels()):
            corpus_subset.add(corpush_obj);
    return corpus_subset;              