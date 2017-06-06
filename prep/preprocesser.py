#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on 2014-01-18

@author: Wei
'''
import subprocess
#import paths
#from document.sentence import Sentence
#from document.token import Token
#from trees.lexicalized_tree import LexicalizedTree
#import prep_utils
import os.path
#from syntax_parser import SyntaxParser
#from document.dependency import Dependency
import re

class Preprocesser:
    def __init__(self):        
        self.max_sentence_len = 100
    
    def heuristic_sentence_splitting(self, raw_sent):
        if len(raw_sent) == 0:
            return []
        
        if len(raw_sent.split()) <= self.max_sentence_len:
            return [raw_sent]
  
        i = len(raw_sent) / 2
        j = i
        k = i + 1
        boundaries = [';', ':', '!', '?']
        
        results = []
        while j > 0 and k < len(raw_sent) - 1:
            if raw_sent[j] in boundaries:
                l_sent = raw_sent[ : j + 1]
                r_sent = raw_sent[j + 1 : ].strip()
                
                if len(l_sent.split()) > 1 and len(r_sent.split()) > 1:
                    results.extend(self.heuristic_sentence_splitting(l_sent))
                    results.extend(self.heuristic_sentence_splitting(r_sent))
                    return results
                else:
                    j -= 1
                    k += 1
            elif raw_sent[k] in boundaries:
                l_sent = raw_sent[ : k + 1]
                r_sent = raw_sent[k + 1 : ].strip()
                
                if len(l_sent.split()) > 1 and len(r_sent.split()) > 1:
                    results.extend(self.heuristic_sentence_splitting(l_sent))
                    results.extend(self.heuristic_sentence_splitting(r_sent))
                    return results
                else:
                    j -= 1
                    k += 1
            else:
                j -= 1
                k += 1
        
        if len(results) == 0:
            return [raw_sent]

                

    def sentence_splitting(self, raw_filename, doc):
        doc.sentences = []
        
        cmd = 'perl boundary.pl -d HONORIFICS -i %s' %(os.path.abspath(raw_filename))

        p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        output, errdata = p.communicate()

        if len(errdata) == 0:
            raw_paras = output.strip().split('\n\n')
            seg_sents = []
            for raw_string in raw_paras:
                raw_sentences = raw_string.split('\n')
                for (i, raw_sent) in enumerate(raw_sentences):
                    if len(raw_sent.split()) > self.max_sentence_len:
                        chunked_raw_sents = self.heuristic_sentence_splitting(raw_sent)
                        if len(chunked_raw_sents) == 1:
                            continue
                        
                        for (j, sent) in enumerate(chunked_raw_sents):
                            seg_sents.append((sent, i == len(raw_sentences) - 1 and j == len(chunked_raw_sents)))		
                            
                    else:
                        seg_sents.append((raw_sent, i == len(raw_sentences) - 1))
	    doc.sentences = seg_sents

        else:
            raise NameError("*** Sentence splitter crashed, with trace %s..." % errdata)
        
            #self.process_single_sentence(doc, raw_text, end_of_para)
        
                

    def preprocess(self, raw_filename, doc):
        self.sentence_splitting(raw_filename, doc)
        
