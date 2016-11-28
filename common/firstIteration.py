# -*- coding: utf-8 -*-
"""
Created on Sat Oct 18 16:58:21 2014

@author: omar
"""

from nltk.corpus import genesis, reuters
from nltk.probability import LidstoneProbDist  
from nltk.util import ngrams
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import prepareEnvironment as pev
import nltk
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.corpus import treebank
from nltk.grammar import ContextFreeGrammar, FeatureGrammar
from nltk import load_parser, grammar, parse
from nltk.data import load
import numpy

max_index = lambda e: e.index(max(e))

def trees2productions(trees):
    """ Transform list of Trees to a list of productions """
    productions = []
    for t in trees:
        productions += t.productions()
    return productions

    
def findLHS(wp, key):
    ret = []
    for i, pr in enumerate(wp):
        if pr.lhs() == key:
            ret.append((i,pr))
    return ret


superNovaGrammar = nltk.parse_cfg("""
    S -> NP VP
    PP -> P NP
    NP -> Det N | 'I' | N
    VP -> V NP
    Det -> 'an' | 'my'
    N -> 'elephant' | 'pajamas'
    V -> 'shot' | 'saw'
    P -> 'in'
""")
print superNovaGrammar
def greedy(root, prods, sentence):
    for rule in root.rhs():
        if isinstance(rule,grammar.Nonterminal):
            lhs = findLHS(prods,rule)
            r = max(lhs, key = lambda x:x[1].prob())
            greedy(r[1],prods, sentence)
        else:
            sentence.append(rule)

def viterbi(root, prods, sentence):
    pathProb = 1
    for rule in root.rhs():
        if isinstance(rule,grammar.Nonterminal):
            lhs = findLHS(prods,rule)
            s = [[] for x in range(len(lhs))]
            probs = []
            for i,r in enumerate(lhs):
                probs.append(viterbi(r[1],prods,s[i]))
            
            ind = max_index(probs)
            sentence.append(s[ind])
            pathProb *=  root.prob() * probs[ind]
        else:
            sentence.append(rule)
            return root.prob()
    return pathProb

def probGen(root, prods, sentence):
    for rule in root.rhs():
        if isinstance(rule,grammar.Nonterminal):
            lhs = findLHS(prods,rule)
            x = numpy.random.random(1)
            sr = lhs[0][1].prob()
            for r in lhs:
                if x < sr:
                    probGen(r[1],prods, sentence)
                    break
                sr += r[1].prob()
        else:
            sentence.append(rule)    


sents = ['I shot an elephant', 'I saw an elephant', 'I shot my pajamas', 'I saw my pajamas' ]

parsers = [nltk.ChartParser(superNovaGrammar)] ##TO BE LOOPED OVER
for parser in parsers:
    prods = []
    for sent in sents:
      prods += parser.parse(sent.split()).productions()

    pcfg = nltk.grammar.induce_pcfg(nltk.grammar.Nonterminal('ROOT'), prods)
    print pcfg
    s = []
    g = pcfg.productions()
    p = findLHS(g,nltk.grammar.Nonterminal('S'))
    sentence = []
    greedy(p[0][1],g,sentence)
#    print(sentence)
    sentence2 = []
    viterbi(p[0][1],g,sentence2)
#    print(sentence2)
    sentence3 = []
    probGen(p[0][1],g,sentence3)
#    print(sentence3)
    