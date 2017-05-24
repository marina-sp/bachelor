import re
import sys

if __name__ == "__main__":
    patt = re.compile("^CHAPTER.*?--[_A-Za-z ]+?\._?$", re.DOTALL | re.MULTILINE)
    
    textid = int (sys.argv[1])
    text = open("../data/id_texts/%02d.txt"%textid,"r").read()
    newtext = re.sub(patt, "", text)
    newfile = open("%02d"%textid, "w")
    newfile.write(newtext)
    newfile.close()
