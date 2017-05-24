from nltk.tokenize import *
from nltk.probability import *
import re
import sys
	
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


def chunk_text(text, size, with_punct):
	if with_punct:
		tokenized_sents = [word_tokenize(sent.lower()) for sent in sent_tokenize(text)]
	else:
		tokenized_sents = [word_tokenize(punct.sub("",sent.lower())) for sent in sent_tokenize(text)]
	
	#print(tokenized_sents[:1])
	
	current_size = 0
	current_chunk = []
	chunks = []
	
	for sent in tokenized_sents:
		sent_size = len(sent)
		"""take the sent only if it reduces the difference from the given size """
		#if (size - current_size) >= (current_size + sent_size - size):
		if current_size < size: 
			current_size += sent_size
			current_chunk.append(sent)
		else:
			chunks.append(current_chunk)
			current_chunk = [sent]
			current_size = sent_size
	# take the last chunk if the last it is 0.9 size or more
	if current_size >= size:
		chunks.append(current_chunk)
	return chunks
	
if __name__ == "__main__":
	#count_words(sys.argv[1])
	#print(chunk_text("Hello. It's me. Please chunk me into pieces.",int(sys.argv[1])))
	files = open("filenames.txt", "r").readlines()
	
	chunks_for_file = []
	chunks_for_file_original = [78,183,383,377,203,167,92,126,156,103,164,261,127,183,173,140,106,68,67]
	
	for file in files:
		text = open("../data/short_books/" + file.strip()).read().replace("\n"," ").replace("\r"," ").decode('utf-8')[1]
		
		#print(file.strip())
		
		chunked = chunk_text(text,int(sys.argv[1]),int(sys.argv[2]))
		num = len(chunked)
		chunks_for_file.append(num)
		
		""" #uncomment to calc average chunk length
		average = 0
		for chunk in chunked:
			average += len(chunk)
			
		#print ("%d chunks with average length of %d\n"%(num, average/num))
		"""
		print(num)

	avg = 0
	for v1,v2 in zip(chunks_for_file,chunks_for_file_original):
		avg += abs(v1-v2)
	print("Chunk size: %d. Average deviation: %d"%(int(sys.argv[1]), avg//len(chunks_for_file)))
		
