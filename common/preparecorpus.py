# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 14:17:42 2014

@author: omar
"""

from nltk.corpus import genesis, reuters
from nltk.probability import LidstoneProbDist  
from nltk.model import NgramModel
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import prepareEnvironment as pev
import nltk
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.corpus import treebank
from nltk.grammar import ContextFreeGrammar, FeatureGrammar
from nltk import load_parser, grammar, parse
from nltk.data import load
import utils

def trees2productions(trees):
    """ Transform list of Trees to a list of productions """
    productions = []
    for t in trees:
        productions += t.productions()
    return productions


#grammar = load('grammars/book_grammars/feat1.fcfg')
##        
#tokens = 'who do you claim that you like'.split()
##tokens = 'I saw the man with my telescope'.split();
#
#parser = nltk.parse.FeatureChartParser
#parser = parser(grammar, trace = 0, chart_class = nltk.parse.FeatureChart)
#print parser.parse(tokens)

#pcfg = nltk.grammar.induce_pcfg(nltk.grammar.Nonterminal('ROOT'), grammar.productions())
#parser = nltk.parse.ViterbiParser(parse.toy_pcfg1, trace=1)

#print parser.parse(tokens)

#tbank_productions = set(production for sent in treebank.parsed_sents()
#                        for production in sent.productions())
#tbank_grammar = ContextFreeGrammar(Nonterminal('S'), list(tbank_productions))

#mini_grammar = ContextFreeGrammar(Nonterminal('S'),
#                                  treebank.parsed_sents()[0].productions())
#parser = nltk.parse.EarleyChartParser(mini_grammar)
#print parser.parse(treebank.sents()[0])



#viterbi_parser = parse.PCFGViterbiParser.train(open('/home/omar/SuperNovaNLG/corpora/corpora/treebank/parsed/wsj_0001.prd', 'r'), root='ROOT')
# 
#t = viterbi_parser.parse(
#nltk.word_tokenize('Numerous passing references to the phrase have occurred in movies'))
# 
#print t
#t.draw()


#superNovaCorpus = pev.CorpusDir + '/corpora/SuperNovaCorpus' # Directory of corpus.
##
#newcorpus = PlaintextCorpusReader(superNovaCorpus, '.*')
#
#
#tokens = list(newcorpus.words('test.txt'))
#parser.parse(tokens)

#print parser.parse(tokens)

##tokens.extend(list(genesis.words('english-kjv.txt')))
##
tokens = list(genesis.words('english-kjv.txt'))  
#tokens.extend(list(reuters.words(categories = 'trade')))  
###  
### estimator for smoothing the N-gram model  
estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
##
### N-gram language model with 3-grams  
model = NgramModel(3, tokens, estimator)  
###  
### Apply the language model to generate 50 words in sequence  
text_words = model.generate(50)
###  
#### Concatenate all words generated in a string separating them by a space.  
text = ' '.join([word for word in text_words])
###
print text
#
#t = treebank.parsed_sents('wsj_0001.mrg')[0]
#t.draw()
#
#treebank.words('test.prd')