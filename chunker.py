from nltk.tokenize import *
from nltk.probability import *
import re
import sys
	
punct = re.compile("[,\.:;\"\?!\[\]\(\)-\*]+")
	
def count_words(text_dir):
	# count lexical words in files 
	# punctuation is ignored 
	files = open("filenames.py", "r").readlines()
	for file in files:
		text = open(text_dir + file.strip()).read().replace("\n"," ").replace("\r"," ") #decode('utf-8')
		tokens = word_tokenize(text)
		words = [word for word in filter(lambda s: not punct.match(s), tokens)]
		print(file.strip() + " " + str(len(tokens)) + " " + str(len(words)) + "\n")


def chunk_text(text, size):
	#tokenized_sents = [word_tokenize(punct.sub("",sent.lower())) for sent in sent_tokenize(text)]
	tokenized_sents = [word_tokenize(sent.lower()) for sent in sent_tokenize(text)]
	
	#print(tokenized_sents[:2])
	current_size = 0
	current_chunk = ""
	chunks = []
	
	for sent in tokenized_sents:
		sent_size = len(sent)
		# take the sent only if it reduces the difference from the given size 
		if (size - current_size) >= (current_size + sent_size - size):
		#if current_size < size: 
			current_size += sent_size
			current_chunk += " " + " ".join(sent)
		else:
			chunks.append(current_chunk.strip())
			current_chunk = " ".join(sent)
			current_size = sent_size
	# take the last chunk if the last it is 0.9 size or more
	if current_size >= size:
		chunks.append(current_chunk)
	return chunks
	
if __name__ == "__main__":
	#count_words(sys.argv[1])
	#print(chunk_text("Hello. It's me. Please chunk me into pieces.",int(sys.argv[1])))
	files = open("filenames.py", "r").readlines()
	for file in files:
		text = open("./data/short_books/" + file.strip()).read().replace("\n"," ").replace("\r"," ") #decode('utf-8')
		#print(file.strip())
		chunked = chunk_text(text,int(sys.argv[1]))
		num = len(chunked)
		average = 0
		for chunk in chunked:
			average += len(chunk.split(" "))
		#print ("%d chunks with average length of %d\n"%(num, average/num))
		print(num)