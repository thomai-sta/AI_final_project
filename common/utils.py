# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 18:01:53 2014

@author: omar
"""

from nltk import Tree
import logging
 
 
def corpus2trees(text):
    """ Parse the corpus and return a list of Trees """
    rawparses = text.split("\n\n")
    trees = []
     
    for rp in rawparses:
        if not rp.strip():
            continue
         
        try:
            t = Tree.parse(rp)
            trees.append(t)
        except ValueError:
            logging.error('Malformed parse: "%s"' % rp)
     
    return trees
 
 
def trees2productions(trees):
    """ Transform list of Trees to a list of productions """
    productions = []
    for t in trees:
        productions += t.productions()
    return productions
    
from nltk.grammar import CFG, FeatureGrammar, WeightedGrammar
from nltk.parse.chart import Chart, ChartParser
from nltk.parse.pchart import InsideChartParser
from nltk.parse.featurechart import FeatureChart, FeatureChartParser 
import nltk.data
    
def load_parser(grammar_url, trace=0, 
                parser=None, chart_class=None, 
                beam_size=0, **load_args):

    grammar = nltk.data.load(grammar_url, **load_args)
    if not isinstance(grammar, ContextFreeGrammar):
        raise ValueError("The grammar must be a ContextFreeGrammar, "
                         "or a subclass thereof.")
    if isinstance(grammar, WeightedGrammar):
        if parser is None: 
            parser = InsideChartParser
        return parser(grammar, trace=trace, beam_size=beam_size)
    
    elif isinstance(grammar, FeatureGrammar):
        if parser is None: 
            parser = FeatureChartParser
        if chart_class is None: 
            chart_class = FeatureChart
        return parser(grammar, trace=trace, chart_class=chart_class)
    
    else: # Plain ContextFreeGrammar.
        if parser is None: 
            parser = ChartParser
        if chart_class is None: 
            chart_class = Chart
        return parser(grammar, trace=trace, chart_class=chart_class)