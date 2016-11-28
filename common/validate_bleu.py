# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 17:14:11 2014

@author: haseeb

http://en.wikipedia.org/wiki/Levenshtein_distance
"""


from __future__ import division;

import corporaRead;
import corpora_reader;
import bleu

def validate():
    methods = ["randGen", "greedy", "viterbi" , "probGen", "ngram"];
#    methods = ["ngram"];
    parsers = ["ChartParser", "RecursiveDescentParser"]
#    , "EarleyChartParser", "BottomUpParser", "TopDownParser"];    
    for parser in parsers:
        for method in methods:        
            validate_(method, parser);
            
def validate_(method, parser):
    print "Method : " + method + " Parser: " + parser;
    
    print "se"
    print "batch 1";
    validate_corpora_star("../corpora/Our_corpora/wardrobe_corpus/split_corpora/batch1_training.txt","../corpora/Our_corpora/wardrobe_corpus/split_corpora/batch1_validation.txt", method, parser);
    print "batch 2";
    validate_corpora_star("../corpora/Our_corpora/wardrobe_corpus/split_corpora/batch2_training.txt","../corpora/Our_corpora/wardrobe_corpus/split_corpora/batch2_validation.txt", method, parser);
    print "batch 3";
    validate_corpora_star("../corpora/Our_corpora/wardrobe_corpus/split_corpora/batch3_training.txt","../corpora/Our_corpora/wardrobe_corpus/split_corpora/batch3_validation.txt", method, parser);   
    
#    print "se_omar"
#    print "batch 1";
#    validate_corpora("../corpora/Our_corpora/wardrobe_corpus/split_corpora/batch1_training.txt","../corpora/Our_corpora/wardrobe_corpus/split_corpora/batch1_validation.txt", method, parser);
#    print "batch 2";
#    validate_corpora("../corpora/Our_corpora/wardrobe_corpus/split_corpora/batch2_training.txt","../corpora/Our_corpora/wardrobe_corpus/split_corpora/batch2_validation.txt", method, parser);
#    print "batch 3";
#    validate_corpora("../corpora/Our_corpora/wardrobe_corpus/split_corpora/batch3_training.txt","../corpora/Our_corpora/wardrobe_corpus/split_corpora/batch3_validation.txt", method, parser);



def validate_corpora(training_corpora, validation_corpora, method, parser):
    # train the generator
    reload(corporaRead);
    corporaRead.init(training_corpora);
    
    # load the validation corpora
    reload(corpora_reader);
    corpora_reader.init(validation_corpora);
    
    error_sum = 0;
    # for all the sentences in the validation corpora 
    uniqueTags = getUniqueTags(corpora_reader.get_corpus_as_list())
    for tags in uniqueTags:
        # generate a sentence using the generator
        gen_sent =  corporaRead.gen_tip(tags, method, parser);
        
        # claculate the distance from ones in the validation corpus, and get the minimum distance
        #print "--------------------------";
#        print tags 
#        print "Generated : ";
#        print gen_sent
#        print [o.getSentences().strip().split() for o in corpora_reader.get_corpus_subset_intersect(tags)]
        
        weights = [0.25,0.25,0.25,0.25]
        if method == "probGen" or method == "randGen":
            tmpE = 0
            for i in range(30):
                tmpE += bleu.BLEU.compute(gen_sent,[o.getSentences().strip().split() for o in corpora_reader.get_corpus_subset_intersect(tags)], weights)
            error_sum += tmpE/30
        else:
            if method == "ngram":
                gen_sent = gen_sent.strip().split()
            error_sum += bleu.BLEU.compute(gen_sent,[o.getSentences().strip().split() for o in corpora_reader.get_corpus_subset_intersect(tags)], weights)
#        print error;
            
    print error_sum / len(uniqueTags);

def getUniqueTags(corpusObjects):
    labels = [o.getLabels() for o in corpusObjects]
    for l in enumerate(labels):
        labels[l[0]].sort()
    
    return [list(t) for t in list(set([tuple(l) for l in labels]))]
    
def validate_corpora_star(training_corpora, validation_corpora, method, parser):
    """
    with Omar's tweak
    """
    # train the generator
    reload(corporaRead);
    corporaRead.init(training_corpora);
    
    # load the validation corpora
    reload(corpora_reader);
    corpora_reader.init(validation_corpora);
    
    gen_error_sum = 0;
    uniqueTags = getUniqueTags(corpora_reader.get_corpus_as_list())
    weights = [0.25,0.25,0.25,0.25]
    for tags in uniqueTags:        
        test_sents = [o.getSentences().strip().split() for o in corpora_reader.get_corpus_subset_intersect(tags)]
        train_sents = [o.getSentences().strip().split() for o in corporaRead.get_corpus_subset_intersect(tags)]
        tagError = 0        
        for sent in test_sents:
            error = bleu.BLEU.compute(sent, train_sents, weights);

            tagError += error;            

        gen_error_sum += tagError/len(test_sents)
    print gen_error_sum / len(uniqueTags);        
          
    

def get_min_edit_dist(target_sentence, sentences_list):
    """
    usage:
        validate_string_edit.get_min_edit_dist("wear your rain boots",["wear your boot", "wear your bijamas", "wear your rain boot shoe"])
        2
    """
    min_dist = 100;
#    print "Golden : ";
    for sentence in sentences_list:
#        print sentence.getSentences();
        
        edit_dist = calc_edit_dist(target_sentence, sentence.getSentences().split());
        if edit_dist < min_dist:
            min_dist = edit_dist;
    return min_dist;


def calc_edit_dist(s,t):
    """
    claculate the string edit distance between two sentences
    usage:
        validate_string_edit.calc_edit_dist("wear your rain boots","wear your boots")
        1
    """
    len_s = len(s);
    len_t = len(t);
    return leven_dist_sentence(s,len_s,t,len_t);
    
def leven_dist_sentence(s,len_s,t,len_t):
    """
    usage:
        validate_string_edit.leven_dist_sentence(["test", "sentence"],2,["test", "sent"],2)
        1
    """
    if len_s == 0:
        return len_t;
    if len_t == 0:
        return len_s;
    
    if s[len_s-1] == t[len_t-1]:
        cost = 0;
    else:
        cost = 1;
    return min(leven_dist_sentence(s, len_s - 1, t, len_t) + 1, leven_dist_sentence(s, len_s, t, len_t-1) + 1, leven_dist_sentence(s, len_s - 1, t, len_t - 1) + cost);