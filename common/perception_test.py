# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 17:09:11 2014

@author: varsha
"""

import corporaRead as cr
import re

def perception_test():
    cr.init('../corpora/Our_corpora/wardrobe_corpus/wardrobe_new_format.txt');
    tag = [['sunny','cloudy'],['windy','calm'],['rainy','dry'],['hot','cold','warm']];
    f = open('../corpora/Our_corpora/wardrobe_corpus/complete_data.txt','r');
    g = open('../corpora/Our_corpora/wardrobe_corpus/perceptiontest.txt','wb');
     
    tag_list = []
    for i in tag[0]:
        for j in tag[1]:
            for k in tag[2]:
                for l in tag[3]:
                    tag_list = [i,j,k,l]
#                    print tag_list
                    tagLabel = tag_list[0]+"/"+tag_list[1]+"/"+tag_list[2]+"/"+tag_list[3]
                    vtxt=cr.gen_tip(tag_list,modelName='viterbi');
                    strV = ' '.join(vtxt)
                    greedytxt=cr.gen_tip(tag_list,modelName='greedy');
                    strG = ' '.join(greedytxt)
                    ptxt=cr.gen_tip(tag_list,modelName='probGen');
                    strP = ' '.join(ptxt)
                    rtxt=cr.gen_tip(tag_list,modelName='randGen');
                    strR = ' '.join(rtxt)
                    g.write('\n')
                    g.write("**************************************************");
                    g.write('\n')                    
                    g.write("viterbi:   ")
                    g.write(tagLabel)
                    g.write(" - ")
                    g.write(strV)
                    g.write('\n')
                    g.write("greedy:   ")
                    g.write(tagLabel)
                    g.write(" - ")
                    g.write(strG)
                    g.write('\n')
                    g.write("probGen:   ")
                    g.write(tagLabel)
                    g.write(" - ")
                    g.write(strP)
                    g.write('\n')
                    g.write("randGen:   ")
                    g.write(tagLabel)
                    g.write(" - ")
                    g.write(strR)   
                    g.write('\n')
                    f.seek(0,0)
                    for line in f:
                        cleanedline = line.strip();  
#                        print "file"
                        if(cleanedline):
                            labelSentList = re.split('-',cleanedline)
                            tmpList = re.split('/',labelSentList[0]);
                            labelList = []
#                            print tag_list
                            for q in tmpList:
                                labelList.append(q.strip())
                            if (labelList == tag_list):
                                snt = labelSentList
                                vtxt=cr.gen_tip(tag_list,modelName='viterbi');
                                vtxt=cr.gen_tip(tag_list,modelName='greedy');
                                vtxt=cr.gen_tip(tag_list,modelName='probGen');
                                vtxt=cr.gen_tip(tag_list,modelName='randGen');
                                                        
                                g.write("human written:   ");
                                g.write(labelSentList[0]);
                                g.write(" - ")
                                g.write(labelSentList[1]);
                                g.write('\n')
                    g.write('\n\n\n\n\n\n');
                    g.write("**************************************************");
#    print humanWritten
    
    