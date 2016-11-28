# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 14:17:42 2014

@author: omar
"""
import os
import nltk
global RootDir

RootDir =  os.path.dirname(os.path.realpath(__file__))
repName = 'SuperNovaNLG'
r = RootDir.find(repName);
RootDir = RootDir[0:r+len(repName)]
nltk.data.path.append(RootDir + '/corpora')
CorpusDir = RootDir + '/corpora'