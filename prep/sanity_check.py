'''
Created on Jul 30, 2014

@author: Vanessa
'''
import paths
import os.path
import subprocess
#from prep.syntax_parser import SyntaxParser
#from classifiers.crf_classifier import CRFClassifier
import traceback
import nltk

#test_filename = '../texts/wsj_0607.out'
#test_filename = 'sample_book.txt'# 
#test_filename = 'jane_austen_emma.txt'
#test_filename = 'waldo_emerson_conduct_of_life.txt'
test_filename = '../../data/id_texts/manual_remove/10.txt'

def check_ssplit():
    cmd = 'perl boundary.pl -d HONORIFICS -i %s' %(os.path.abspath(test_filename))
#        print cmd
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    output, errdata = p.communicate()

    if len(errdata) == 0:
        paras = output.strip().split('\n\n')
        sents = []
        for (i, para) in enumerate(paras):
            #print 'Paragraph #%d' % (i + 1)
            para_sents = para.split('\n')
            '''for sent in para_sents:
                print sent
            print'''
            
            sents.extend(para_sents)
        
        print "Successfully split the test file into %d paragraphs and %d sentences." % (len(paras), len(sents))
        
        return sents
    else:
        raise NameError("*** Sentence splitter crashed, with trace %s..." % errdata)
    

def check_syntax_parser(sents):
    syntax_parser = None
    try:
        syntax_parser = SyntaxParser()
    except Exception, e:
        print "*** Loading Stanford parser failed..."
        raise e
    output = []
    for (i, sent) in enumerate(sents):
        try:
	    if len(sent)==0:
		continue
            const_tree, dep_tree = syntax_parser.parse_sentence(sent)
	    #print const_tree
	    parse_tree = nltk.Tree.fromstring(const_tree)
	    tokens = parse_tree.leaves()
            output.append(' '.join(tokens))
            print 'Parsing sentence %d successful' % (i + 1)
        except Exception, e:
            print "sent: %s"%sent
            raise NameError("*** Parsing sentence %d failed" % (i + 1))

    if syntax_parser:
        syntax_parser.unload()
    with open('tokens.txt','wb') as tok:
        tok.write('\n'.join(output))


def check_CRFSuite():
    crfsuite_test_file = os.path.join(paths.CRFSUITE_PATH, 'test.txt')
    vectors = open(crfsuite_test_file).read().strip().split('\n')
    for (model_name, model_type, model_path, model_file) in [('segmentation', 'segmenter', paths.SEGMENTER_MODEL_PATH, 'seg.crfsuite'),
                                     ('segmentation 2nd pass', 'segmenter', paths.SEGMENTER_MODEL_PATH, 'seg_global_features.crfsuite'),
                                     ('treebuilding intra-sentnetial structure', 'treebuilder', paths.TREE_BUILD_MODEL_PATH, 'struct/intra.crfsuite'),
                                     ('treebuilding multi-sentnetial structure', 'treebuilder', paths.TREE_BUILD_MODEL_PATH, 'struct/multi.crfsuite'),
                                     ('treebuilding intra-sentnetial relation', 'treebuilder', paths.TREE_BUILD_MODEL_PATH, 'label/intra.crfsuite'),
                                     ('treebuilding multi-sentnetial relation', 'treebuilder', paths.TREE_BUILD_MODEL_PATH, 'label/multi.crfsuite')]:
        try:
            print '*** Loading classifier %s...' % model_name
            classifier = CRFClassifier(model_name, model_type, model_path, model_file, False)
            classifier.classify(vectors)
            classifier.unload()
        except Exception, e:
            raise e
                            

    
    
import sys

if __name__ == '__main__':
    c_ssplit = True
    c_ssparse = False
    c_crfsuite = False
    
    steps = 1
    if c_ssplit or c_ssparse:
        print '********** Step %d: Now checking sentence splitting module...' % steps
        try:
            sents = check_ssplit()
            print sents[:10]
            with open('sents.txt','wb') as s:
                s.write('\n'.join(sents))
            steps += 1
        except Exception, e:
            traceback.print_exc()
            sys.exit(1)

    if c_ssparse:
        print '********** Step %d: Now checking syntactic parsing module...' % steps
        try:
            check_syntax_parser(sents)
            print
            steps += 1
        except Exception, e:
            traceback.print_exc()
            sys.exit(1)
        
    if c_crfsuite:
        print '********** Step %d: Now checking CRFSuite classification module...' % steps
        try:
            check_CRFSuite()
            print
            steps += 1
        except Exception, e:
            traceback.print_exc()
            sys.exit(1)
