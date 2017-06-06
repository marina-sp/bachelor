#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nltk.tokenize import *
from nltk.probability import *
import bllipparser
import re
import sys
from unicodedata import normalize
import codecs

from doc import Document as D
from preprocesser import Preprocesser as P
	
punct = re.compile("[,\.:;\"\?!\[\]\(\)-\*]+")

def build_paras(text, tokenize_function):
	# use nltk for sentence and word splitting
	if isinstance(text, unicode):
		pass
		#print("unicode input!")
	paras = filter(lambda p: re.search("\w+",p), text.encode('utf-8').split("\n\n"))
	for para in paras:
		if isinstance(para, unicode):
			pass
			#print("oh no, unicode again!!")
	tp = []
	for para in paras:
		sents = [sent.replace("\n"," ").strip() for sent in sent_tokenize(para)]
		#print(sents)
		tok_sents = [tokenize_function(sent) for sent in sents]	
		tp.append(tok_sents)
		
	#tokenized_paragraphs = map(lambda paragraph: [tokenize_function(sent) for sent in sent_tokenize(paragraph)], paragraphs)
	#print(tp[0][0])	
	return tp

def build_paras_with_rst(filename, tokenize_function):
	# use preprocessing from RST parser to split sentences

	doc = D()
	doc.preprocess(filename, P())

	paragraphs = []
	current_para = []
	for sent, end_of_para in doc.sentences:
		if not re.search("\w+",sent):
			continue
		current_para.append(tokenize_function(sent))	
		if end_of_para:
			paragraphs.append(current_para)
			current_para = []
	return paragraphs
	
	

def chunk(paragraphs, size, no_par_breaks):
	#print(len(paragraphs), size, no_par_breaks)
	current_size = 0
	current_chunk = []
	chunks = []
	if no_par_breaks == True:
		units = paragraphs
		size_of = lambda para: reduce(lambda len1,len2: len1 + len2, map(lambda sent: len(sent), para))
		merge = lambda chunk, para: chunk + para
	else:
		units = [sent for para in paragraphs for sent in para]
		size_of = len
		merge = lambda chunk, sent: chunk + [sent]
	#print(units[:5])
	for unit in units:
		unit_size = size_of(unit)
		#print(unit_size)
		if current_size < size: 
			current_size += unit_size
			current_chunk = merge(current_chunk,unit)
		else:
			chunks.append(current_chunk)
			current_chunk = []
			current_chunk = merge(current_chunk, unit)
			current_size = unit_size
		#print(current_chunk[:5])

	# take the last chunk 
	if (current_size >= 1000)and(current_size >= size):
		chunks.append(current_chunk)
	return chunks

def split(string):
	return string.split()

def chunk_one(fileid, size, tokenizer, no_par_breaks, rst, mydir = "../../data/id_texts/ascii_texts/"):
	if tokenizer == "split":
	 	split_words = split
	elif tokenizer == "nltk_nop":
		split_words = lambda sent: word_tokenize(punct.sub("",sent))
	elif tokenizer == "nltk":
		split_words = lambda sent: word_tokenize(sent)	
	elif tokenizer == "bllip_nop":
		split_words = lambda sent: bllipparser.tokenize(punct.sub("",sent))
	elif tokenizer == "bllip":
		split_words = lambda sent: bllipparser.tokenize(sent)
	
	if rst:
		paras = build_paras_with_rst(mydir + "%02d.txt"%fileid, split_words)
	else:
		text = codecs.open(mydir + "%02d.txt"%fileid,"r","utf-8").read()[3:]	
		paras = build_paras(text, split_words)
	#print(paras[:2])
	chunks = chunk(paras, size, no_par_breaks)
	#print(len(chunks))
	return chunks



def chunk_all(size, tokenizer, no_par_breaks, rst, print_long = False):
	chunks_for_file = []
	chunks_for_file_original = [78,183,383,377,203,167,92,126,156,103,164,261,127,183,173,140,106,68,67]
	chunks_for_file_exp = [62,165,343,340,173,158,81,109,138,94,148,196,112,146,149,114,93,60,62]
	
	for i in range(1,20):
		chunks = chunk_one(i, size, tokenizer, no_par_breaks, rst)
		chunks_for_file.append(len(chunks))

	avg = 0
	avg1 = 0
	for v1,v2,v3 in zip(chunks_for_file,chunks_for_file_exp,chunks_for_file_original):
		avg += abs(v1-v2)
		avg1 += abs(v1-v3)
	avg = avg * 1.0 / len(chunks_for_file)
	avg1 = avg1 * 1.0/ len(chunks_for_file)
	if print_long:
		for f in chunks_for_file:
			print(f)
	if (avg < 8.0) or (avg < 8.0) or (print_long):
		print("Chunk size: %d. Tokenizer: %s. No para breaks: %r. RST parser: %r. \nAverage deviation from new dateset: %.2f.\nAverage deviation from old dataset: %.2f.\n"%(size, tokenizer, no_par_breaks, rst, avg, avg1))
	return

def split_in_chap(fileid):
	text = codecs.open("../../data/id_texts/ascii_texts/chapters/%02d/CH%02d.txt"%(fileid,fileid),"r","utf-8").read()	
	chaps = text.split("CHAPTER")
	for i,chap in enumerate(chaps):
		out = open("../../data/id_texts/ascii_texts/chapters/%02d/%02d_CH%02d.txt"%(fileid,fileid,i),"w")
		out.write(chap)
	return len(chaps)

if __name__ == "__main__":
	# EXAMPLE: python chunker.py all SIZE TOKENIZER NO_PAR_BREAKS RST

	#count_words(sys.argv[1])
	#print(chunk_text("Hello. It's me. Please chunk me into pieces.",int(sys.argv[1])))
	if sys.argv[1] == "all":
		#chunk_all(int(sys.argv[2]), bool(int(sys.argv[3])))
		chunk_all(int(sys.argv[2]), sys.argv[3], bool(int(sys.argv[4]))	, bool(int(sys.argv[5])), True)
		
	elif sys.argv[1] == "one":
		chunks= chunk_one(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], bool(int(sys.argv[5])), bool(int(sys.argv[6])))
		# for first 10 chunks print 10 first sentences and length of the chunk		
		#for i in range(10):
			#print len(chunks[i])
			#print chunks[i][:10]
	elif sys.argv[1] == "test":
		for size in range(950,1060,10):
			for tokenizer in ["split","nltk_nop","nltk","bllip_nop","bllip"]:
				for no_par_breaks in [True,False]:
					for rst in [True,False]:
						try:
							chunk_all(size,tokenizer,no_par_breaks,rst)
						except:
							print("Failed on: %d %s %r %r.\n"%(size,tokenizer,no_par_breaks,rst))
	elif sys.argv[1] == "chapter":
		for fid in range(1,9):
			n = split_in_chap(fid)
			sum_all = 0
			for chapid in range(n):
				chunks = chunk_one(chapid, int(sys.argv[2]), sys.argv[3], bool(int(sys.argv[4])), bool(int(sys.argv[5])), "../../data/id_texts/ascii_texts/chapters/%02d/%02d_CH"%(fid,fid))
				sum_all += len(chunks)
				#print("File %d chapter %d: %d"%(fid, chapid, len(chunks)))
			print("File %d: %d"%(fid, sum_all))
