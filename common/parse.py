# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 18:02:34 2014

@author: omar
"""

import nltk
from nltk.grammar import WeightedProduction, Nonterminal
from utils import corpus2trees, trees2productions
 
 
class PCFGViterbiParser(nltk.ViterbiParser):
    def __init__(self, grammar, trace=0):
        super(PCFGViterbiParser, self).__init__(grammar, trace)
     
    @staticmethod
    def _preprocess(tokens):
        replacements = {
        "(": "-LBR-",
        ")": "-RBR-",
        }
        for idx, tok in enumerate(tokens):
            if tok in replacements:
                tokens[idx] = replacements[tok]

        return tokens
         
    @classmethod
    def train(cls, content, root):
        if not isinstance(content, basestring):
            content = content.read()
         
        trees = corpus2trees(content)
        productions = trees2productions(trees)
        pcfg = nltk.grammar.induce_pcfg(nltk.grammar.Nonterminal(root), productions)
        return cls(pcfg)
     
    def parse(self, tokens):
        tokens = self._preprocess(list(tokens))
        tagged = nltk.pos_tag(tokens)
         
        missing = False
        for tok, pos in tagged:
            if not self._grammar._lexical_index.get(tok):
                missing = True
                self._grammar._productions.append(WeightedProduction(Nonterminal(pos), [tok], prob=0.000001))
            if missing:
                self._grammar._calculate_indexes()
             
        return super(PCFGViterbiParser, self).parse(tokens)