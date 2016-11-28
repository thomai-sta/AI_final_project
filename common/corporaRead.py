# -*- coding: utf-8 -*-
"""
Created on Sat Oct 18 17:08:10 2014

@author: varsha
"""
import nltk;

import re;
from nltk import pos_tag,word_tokenize;
from nltk.corpus import wordnet as wn;
from collections import defaultdict;
from nltk import grammar
from nltk.probability import LidstoneProbDist
import numpy
from nltk.model import NgramModel
from sets import Set;

max_index = lambda e: e.index(max(e))

#from nltk.tag.stanford import POSTagger


tag_dict = defaultdict(list);

class corpusDetail:
  labels = [];
  sentences = ' ';
  def getLabels(self):
    return self.labels;
  def getSentences(self):
    return self.sentences;
  def setLabels(self,value):
    self.labels = value;
  def setSentences(self,value):
    self.sentences = value;

sentLabelList = [];
posList = [];
    
corpus_sents = [];

def init(corpus_file):     
    
    if len(sentLabelList) != 0:
        return;
    tag_types = [['sunny','cloudy'],['windy','calm'],['rainy','dry'],['hot','cold','warm']];   
    f = open(corpus_file,'r');
    g = open('../corpora/Our_corpora/wardrobe_corpus/complete_data.txt','wb');
    labelSentList = [];
    
    for line in f:
      cleanedline = line.strip()
      if(cleanedline):
        labelSentList = re.split('-',cleanedline)
        tmpList = re.split('/',labelSentList[0]);
        labelList = []
        for q in tmpList:
          labelList.append(q.strip())
        
        tag = [];
        tag.append([]);
        tag.append([]);
        tag.append([]);
        tag.append([]);
        for x in range(4):
            if(labelList[x] == "*"):
                for y in tag_types[x]:
                    tag[x].append(y);
            else:
                tag[x].append(labelList[x]);
    
        for i in tag[0]:
            for j in tag[1]:
                for k in tag[2]:
                    for l in tag[3]:
                        lbl = [i,j,k,l];
                        sentence = lbl[0]+'/'+lbl[1]+'/'+lbl[2]+'/'+lbl[3]
                        sentence += '-'
                        sentence += labelSentList[1]+'\n'
                        g.write(sentence);
                        corpusObject = corpusDetail();
                        corpusObject.setLabels(lbl);
                        corpusObject.setSentences(labelSentList[1]); 
                        sentLabelList.append(corpusObject);
    

    for obj in sentLabelList:
        sentence = obj.getSentences();
        lexicalization(sentence);

    print "Gen initialized"

def uniq_words_count():
    uniq_words = Set([]);
    total_words = [];
    for sent in sentLabelList:
        print sent.getSentences();
#        words = sent.getSentences().split();
#        for word in words:
#            print word;
#            uniq_words.add(word);
#            total_words.append(word);
#    print uniq_words;
#    print total_words;
#    print len(total_words);
#    print len(uniq_words);
    
def input_read(input_date,genName, parserName):
#    import corporaRead
#    cr.input_read('2014/10/26','probGen','ChartParser')
    init('../corpora/Our_corpora/wardrobe_corpus/wardrobe_new_format.txt');
    f = open('../corpora/Our_corpora/wardrobe_corpus/input_data.txt','r');
    in_data = []
    for line in f:
        cleanedline = line.strip()
        if(cleanedline):
            date_input = re.split('-',cleanedline);
            date = date_input[0];
            date = date.split();
#            print date
#            print input_date
            if(date[0] == input_date):
#                print "test"
                weather_data = date_input[1];
#                weather_data = weather_data.split();
                weather_data = re.split(',',weather_data);
                in_data = weather_data                
#                print weather_data

            
    
#    in_data = [20,40,67,57]
#    print in_data
    out_tags = []
    cloud = int(in_data[0]);
    wind = int(in_data[1]);
    rain = int(in_data[2]);
    temp = int(in_data[3]);
    if (cloud > 50):
        out_tags.append('cloudy');
    else:
        out_tags.append('sunny');
    
    if(wind > 38):
        out_tags.append('windy');
    else:
        out_tags.append('calm');

    if(rain > 50):
        out_tags.append('rainy');
    else:
        out_tags.append('dry');
    
    if(temp < 10):
        out_tags.append('cold');
    elif(temp > 20):
        out_tags.append('hot');
    else:
        out_tags.append('warm');
    snt = gen_tip(out_tags,modelName = genName ,parserName = parserName)
    print out_tags
    text = ' '.join([word for word in snt])
    print text    
    
    

def get_corpora_objects():
    return sentLabelList;
    
def lexicalization(text):
  token = word_tokenize(text);
  posList.extend(nltk.pos_tag(token));
    
    
    
def  get_corpus_sents():
    return corpus_sents;

  
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
    usage: corporaRead.get_corpus_subset(["sunny", "hot"])
    return a subset of the corpus; intersect of all sentences that has one of the tags specified in tags_list
    """
    corpus_subset = Set([]);
    for corpush_obj in sentLabelList:
        if set(tags_list) == set(corpush_obj.getLabels()):
            corpus_subset.add(corpush_obj);
    return corpus_subset;        
    
def buildGrammar(posList):
# Rules
  cfg = """ S -> S1
S1 -> VP NP | DATE PRP VP1 NP | PRP VP1 NP
VBTO -> VBP TO | DON VBP TO
VP1 -> MD VB | MD RB VB | VBTO VB | 'need' | DON 'need' 
VP -> DATE VB | PV | VB | MD VB | MD PV | MB RB VB | MD RB PV | DON VB
PV -> 'put' IN
DON -> DO RB
NP -> Nom DATE | Nom
Nom -> JJ Noun | PRPS Noun | PRPS JJ Noun | Noun | DT NN | DT JJ Noun | P NNS
Noun -> NN | NNS
P -> 'a' Num 'of' 

"""
  # Read LEXICON
  f = open('../corpora/Our_corpora/wardrobe_corpus/lexicon.txt','r');
  lexicon = [];
  tag = 0;
  for line in f:
    for word in line.split():
      if tag == 0:
        new_word = word;
        tag = 1;
      else:
        new_tag = word;
        tag = 0;
        if new_tag not in tag_dict:
          tag_dict[new_tag].append(new_word);
        elif new_word not in tag_dict.get(new_tag):
          tag_dict[new_tag].append(new_word);
  for tag, words in tag_dict.items():    
    cfg = cfg + tag + " -> "
    first_word = True
    for word in words:
      if first_word:
        cfg = cfg + "\'" + word + "\'"
        first_word = False
      else:
        cfg = cfg + " | \'" + word + "\'"
    cfg = cfg + '\n'
      
  return cfg

def build_cfg():
    cfg = buildGrammar(posList);
    cfg = nltk.parse_cfg(cfg);
#    print cfg;
    return cfg;

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
            sr = 0
            for r in lhs:
                sr += r[1].prob()
                if x < sr:
                    probGen(r[1], prods, sentence)
                    break
        else:
            sentence.append(rule)

def randGen(root, prods, sentence):
    for rule in root.rhs():
        if isinstance(rule,grammar.Nonterminal):
            lhs = findLHS(prods,rule)
            x = numpy.random.random_integers(0,len(lhs)-1);
            randGen(lhs[x][1], prods, sentence);
        else:
            sentence.append(rule);    
    
def gen_tip(tags_list, modelName = 'probGen', parserName = 'ChartParser', sentenceCount = 1, N = 2):
    """
    usage:
        wardrope_tips_gen.gen_tip(["rainy", "windy"], model, parserName)
        model can be: 'greedy', 'viterbi', 'probGen', 'ngram'
        parserName can be: 'ChartParser', 'RecursiveDescentParser'
        take your rain coat
    """
    if modelName == 'greedy':
        model = greedy
    elif modelName == 'viterbi':
        model = viterbi 
    elif modelName == 'probGen':
        model = probGen
    elif modelName == 'randGen':
        model = randGen
        
    if modelName != 'ngram':
        if parserName == 'ChartParser':
            parser = nltk.parse.ChartParser(build_cfg())
        elif parserName == 'RecursiveDescentParser':
            parser = nltk.parse.RecursiveDescentParser(build_cfg())
        elif parserName == 'EarleyChartParser':
            parser = nltk.parse.EarleyChartParse(build_cfg())
        elif parserName == 'BottomUpParser':
            parser = nltk.parse.BottomUpChartParse(build_cfg())
        elif parserName == 'TopDownParser':
            parser = nltk.parse.TopDownChartParser(build_cfg())
        
#        sents = get_corpus_subset(tags_list)
        sents = [];
        for o in get_corpus_subset_intersect(tags_list):  
            sents.append(o.getSentences())
            
        prods = []
        for sent in sents:
          prods += parser.parse(sent.split()).productions()

#        print prods;            
        pcfg = nltk.grammar.induce_pcfg(nltk.grammar.Nonterminal('ROOT'), prods)
        g = pcfg.productions()
        p = findLHS(g,nltk.grammar.Nonterminal('S'))
        sentence = []
        model(p[0][1],g,sentence)
        if  modelName == 'viterbi':
            result = [];
            return flatten_veterbi_output(sentence, result);
        return sentence
    else:
        tokens = [];
        for o in get_corpus_subset_intersect(tags_list):  
            tokens.append(o.getSentences())
        estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
        model = NgramModel(N, tokens, estimator)  
        text_words = model.generate(sentenceCount)
        text = ' '.join([word for word in text_words])
        return text
        
def flatten_veterbi_output(array, result):
#    print array;
    if isinstance(array, str):
        return array;
    else:            
        for item in array:
            tmp = flatten_veterbi_output(item, result);
            if isinstance(tmp, str):
                result.append(tmp);
        return result;