#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from unicodedata import normalize


def convert_to_ascii(text):
	ntext = normalize("NFKD",text)
	#print(isinstance(text, unicode))
	to_replace = [(u"—",u"-"),(u"’",u"'"),(u"‘",u"'"),(u"“",u"\""),(u"”",u"\""),(u"é",u"e"),(u"â",u"a"),		 				(u"è",u"e"),(u"ô",u"o"),(u"ö",u"o"),(u"à",u"a"),(u"ê",u"e"),(u"æ",u"ea"),
			(u"⁄",u"/"),(u"£",u""),(u"œ",u"oe"),(u"ç",u"c"),(u"°",u""),(u"\ufeff",u" "),
			(u"û",u"u"),(u"Œ",u""),(u"î",u"i"),(u"ë",u"e"),(u"ï",u"i"),(u"Æ",u"")]	
	clear_text = ntext
	for old,new in to_replace:
		#print(old,new)
		clear_text = clear_text.replace(old,new)	
	return clear_text

if __name__ == "__main__":
	not_ascii = []
	for i in range(1,20):
		text = codecs.open("./manual_remove/%02d.txt"%i,"r","utf-8").read()
		clear_text = convert_to_ascii(text)
		words = clear_text.split()		
		for word in words:
			try: 
				word.encode('ascii')				
			except:
				not_ascii.append((word,i))			
		outfile = codecs.open("./ascii_texts/chapters/%02d/%02d.txt"%(i,i),"w","utf-8")
		outfile.write(clear_text)
	
	for word, textid in not_ascii:
		print("There is a not ascii symbol in '%s' in text %d"%(word,textid))

