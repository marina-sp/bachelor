from nltk.tokenize import *
from nltk.probability import *
from bllipparser import tokenize
import re
import sys

from doc import Document as D
from preprocesser import Preprocesser as P
	
punct = re.compile("[,\.:;\"\?!\[\]\(\)-\*]+")
	
def count_words(text_dir):
	# count lexical words in files 
	# punctuation is ignored 
	files = open("filenames.txt", "r").readlines()
	for file in files:
		text = open(text_dir + file.strip()).read().replace("\n"," ").replace("\r"," ") #decode('utf-8')
		tokens = word_tokenize(text)
		words = [word for word in filter(lambda s: not punct.match(s), tokens)]
		print(file.strip() + " " + str(len(tokens)) + " " + str(len(words)) + "\n")
	return 

def build_paras(text, tokenize_function):
	# use nltk for sentence and word splitting
	
	paragraphs = filter(lambda p: re.search("\w+",p), re.split("\n\n",text.decode("utf-8")))
	
	tokenized_paragraphs = map(lambda paragraph: [tokenize_function(sent) for sent in sent_tokenize(paragraph)], paragraphs)

	return tokenized_paragraphs

def build_paras_with_rst(filename, tokenize_function):
	# use preprocessing from RST parser to split sentences
	# tokenization on " "

	doc = D()
	doc.preprocess(filename, P())

	paragraphs = []
	current_para = []
	for sent, end_of_para in doc.sentences:
		if not re.search("\w+",sent):
			continue
		current_para.append(tokenize_function(sent.decode('utf-8')))	
		if end_of_para:
			paragraphs.append(current_para)
			current_para = []
	return paragraphs
	
	

def chunk(paragraphs, size):
	current_size = 0
	current_chunk = []
	chunks = []
	
	for paragraph in paragraphs:
		par_size = reduce(lambda len1,len2: len1 + len2, map(lambda sent: len(sent), paragraph))
		# take the sent only if it reduces the difference from the given size
		#if (size - current_size) >= (current_size + sent_size - size):
		if current_size < size: 
			current_size += par_size
			current_chunk += paragraph
		else:
			chunks.append(current_chunk)
			current_chunk = paragraph
			current_size = par_size
	# take the last chunk if the last it is 0.9 size or more
	if (current_size >= 1000)and(current_size >= size):
		chunks.append(current_chunk)
	return chunks

def split(string):
	return string.split()

def chunk_all(size, tokenizer, docs = True):
	chunks_for_file = []
	chunks_for_file_original = [78,183,383,377,203,167,92,126,156,103,164,261,127,183,173,140,106,68,67]
	chunks_for_file_exp = [62,165,343,340,173,158,81,109,138,94,148,196,112,146,149,114,93,60,62]
	
	if tokenizer == "split":
	 	split_words = split
	elif tokenizer == "nltk_nop":
		split_words = lambda sent: word_tokenize(punct.sub("",sent))
	elif tokenizer == "nltk":
		split_words = word_tokenize	
	elif tokenizer == "bllip":
		split_words = tokenize
	
	for i in range(1,20):
		
		if docs:
			paras = build_paras_with_rst("../../data/id_texts/manual_remove/%02d.txt"%i, split_words)
		else:
			text = open("../../data/id_texts/manual_remove/%02d.txt"%i).read()		
			paras = build_paras(text, split_words)
		chunked = chunk(paras, size)
		num = len(chunked)
		chunks_for_file.append(num)
		print(num)

	avg = 0
	avg1 = 0
	for v1,v2,v3 in zip(chunks_for_file,chunks_for_file_exp,chunks_for_file_original):
		avg += abs(v1-v2)
		avg1 += abs(v1-v3)
	print("Chunk size: %d. RST parser: %r. Tokenizer: %s. \nAverage deviation from new dateset: %.2f.\nAverage deviation from old dataset: %.2f."%(size, docs, tokenizer, avg*1.0/len(chunks_for_file),avg1*1.0/len(chunks_for_file)))
	return 

if __name__ == "__main__":
	# EXAMPLE: python chunker.py all 1000 nltk_nop

	#count_words(sys.argv[1])
	#print(chunk_text("Hello. It's me. Please chunk me into pieces.",int(sys.argv[1])))
	if sys.argv[1] == "all":
		#chunk_all(int(sys.argv[2]), bool(int(sys.argv[3])))
		chunk_all(int(sys.argv[2]), sys.argv[3])
	elif sys.argv[1] == "text":
		textid = int(sys.argv[1])
		text = open("../data/id_texts/manual_remove/%02d.txt"%textid).read()
		chunks = chunk(build_paras(text), 1000, False)
		print (len(chunks))
	elif sys.argv[1] == "doc":
		chunks = chunk(build_paras_with_rst(sys.argv[2]), int(sys.argv[3]))	
		print(len(chunks))

