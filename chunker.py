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
	return 

def chunk_text(text, size, with_punct):
	
	paragraphs = filter(lambda p: re.search("\w+",p), re.split("\n\n",text.decode("utf-8")))
	
	#print(len(paragraphs))
	#print(paragraphs[:8])
	
	if with_punct:
		tokenized_paragraphs = map(lambda paragraph: [word_tokenize(sent.lower()) for sent in sent_tokenize(paragraph)], paragraphs)		
	else:
		tokenized_paragraphs = map(lambda paragraph: [word_tokenize(punct.sub("",sent.lower())) for sent in sent_tokenize(paragraph)], paragraphs)

	#print(tokenized_paragraphs[6])
	
	current_size = 0
	current_chunk = []
	chunks = []
	
	for paragraph in tokenized_paragraphs:
		par_size = reduce(lambda len1,len2: len1 + len2, map(lambda sent: len(sent), paragraph))
		#print(par_size)
		""" take the sent only if it reduces the difference from the given size """
		#if (size - current_size) >= (current_size + sent_size - size):
		if current_size < size: 
			current_size += par_size
			current_chunk += paragraph
		else:
			chunks.append(current_chunk)
			current_chunk = paragraph
			current_size = par_size
	# take the last chunk if the last it is 0.9 size or more
	if current_size >= size:
		chunks.append(current_chunk)
	#print(chunks[0][:5])
	return chunks

def chunk_all(size, with_punct):
	chunks_for_file = []
	chunks_for_file_original = [78,183,383,377,203,167,92,126,156,103,164,261,127,183,173,140,106,68,67]
	chunks_for_file_exp = [62,165,343,340,173,158,81,109,138,94,148,196,112,146,149,114,93,60,62]
	
	for i in range(1,20):
		text = open("../data/id_texts/%02d.txt"%i).read()
		
		#print(file.strip())
		
		chunked = chunk_text(text, size, with_punct)
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
	for v1,v2 in zip(chunks_for_file,chunks_for_file_exp):
		avg += abs(v1-v2)
	print("Chunk size: %d. Average deviation: %d"%(size, avg//len(chunks_for_file)))
	return 

if __name__ == "__main__":
	#count_words(sys.argv[1])
	#print(chunk_text("Hello. It's me. Please chunk me into pieces.",int(sys.argv[1])))
	"""
	chunk_all(int(sys.argv[1]), int(sys.argv[2]))
	
	"""
	textid = int(sys.argv[1])
	text = open("%02d"%textid).read()
	chunks = chunk_text(text, 1000, 0)
	print (len(chunks))	
	
