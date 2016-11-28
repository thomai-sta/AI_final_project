# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 17:14:11 2014

@author: haseeb

http://en.wikipedia.org/wiki/Levenshtein_distance
"""


from __future__ import division;

import corporaRead;
import corpora_reader;

def validate():
    # batch 1
    print validate_corpora("../corpora/Our_corpora/wardrobe_corpus/split_corpora/batch1_training.txt","../corpora/Our_corpora/wardrobe_corpus/split_corpora/batch1_validation.txt");
    # batch 2
    print validate_corpora("../corpora/Our_corpora/wardrobe_corpus/split_corpora/batch2_training.txt","../corpora/Our_corpora/wardrobe_corpus/split_corpora/batch2_validation.txt");
    # batch 3
    print validate_corpora("../corpora/Our_corpora/wardrobe_corpus/split_corpora/batch3_training.txt","../corpora/Our_corpora/wardrobe_corpus/split_corpora/batch3_validation.txt");



def validate_corpora(training_corpora, validation_corpora):
    # train the generator
    corporaRead.init(training_corpora);
    
    # load the validation corpora
    corpora_reader.init(validation_corpora);
    
    error_sum = 0;
    # for all the sentences in the validation corpora 
    for corpora_sent in corpora_reader.get_corpus_as_list():
        tags = corpora_sent.getLabels();
        # generate a sentence using the generator
        gen_sent =  corporaRead.gen_tip(tags);
        
        # claculate the distance from ones in the validation corpus, and get the minimum distance
        #print "--------------------------";
#        print tags 
#        print "Generated : ";
#        print gen_sent;
        edit_dist = get_min_edit_dist(gen_sent, corpora_reader.get_corpus_subset_intersect(tags));
        if edit_dist > len(gen_sent):
            error  = 1;
        else:
            error = edit_dist/len(gen_sent);
        error_sum = error_sum +  error;
#        print error;
    return error_sum / len(corpora_reader.get_corpus_as_list());
        
        
    

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