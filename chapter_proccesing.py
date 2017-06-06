import re
import sys
from filter_ascii import convert_to_ascii
import codecs

if __name__ == "__main__":
    patt = re.compile("^CHAPTER \d$\n\n", re.DOTALL | re.MULTILINE)
    #patt = re.compile("^CHAPTER [IVXL]+$\n\n^.+?$\n\n", re.DOTALL | re.MULTILINE)
    #patt = re.compile("^\s*[A-Z. ]+?\.?$", re.DOTALL | re.MULTILINE)



    textid = int (sys.argv[1])
    text = convert_to_ascii(codecs.open("../data/id_texts/manual_remove/%02d.txt"%textid,"r","utf-8").read())
    
    newtext = re.sub(patt, "CHAPTER\n\n", text)

    newfile = open("../data/id_texts/ascii_texts/chapters/%02d/CH%02d.txt"%(textid,textid), "w")
    newfile.write(newtext)
    newfile.close()
