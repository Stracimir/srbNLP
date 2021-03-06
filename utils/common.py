import codecs
import re

# Regex for numbers, dates, scores, etc.
NUM_TAG = "<NUM>"
REGEX_NUM = re.compile(r"^(\d+[.,:/\-]?)+$")

# Regex for URLs
URL_TAG = "<URL>"
REGEX_URL = re.compile(r"^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/|www\.)+[a-zA-Z0-9]+([\-\.]{1}[a-zA-Z0-9]+)*\.[a-zA-Z]{2,5}(:[0-9]{1,5})?(\/.*)?$")

# Punctuation
PUNCTUATION = [".",",",":",";","\"","\'","?","!","\\","-","/"]
COMMAS_REGEX = re.compile(r"^,+$")
DOTS_REGEX = re.compile(r"^\.+$")
 
def tokenize (inputFile, outputFile):
    
    with open (inputFile, "r") as fin:
        lines = fin.readlines()
    
    sentences = []
    for line in lines:
        sentences.append("\n".join([word for word in line.split()]))
    
    with open (outputFile, "w") as fout:
        fout.write("\n\n".join(sentences))
        
def glue (inputFile, outputFile):
    
    with open (inputFile, "r") as fin:
        text = fin.read()
    
    lines = [line.replace('\n', ' ') for line in text.split("\n\n")]
    
    with open (outputFile, "w") as fout:
        fout.write('\n'.join(lines))

def filter_(inputFile, outputFile):
    with open (inputFile, "r") as fin:
        lines = fin.readlines()
    
    filtered_lines = []
    for line in lines:
        filtered_words = [word for word in line.split() if ((word not in PUNCTUATION) and (not DOTS_REGEX.match(word)) and (not COMMAS_REGEX.match(word)))]
        filtered_lines.append(' '.join(filtered_words))
    
    with open (outputFile, "w") as fout:
        fout.write('\n'.join(filtered_lines))

def replace_tags(inputFile, outputFile):
    with open (inputFile, "r") as fin:
        lines = fin.readlines()
    
    tagged_lines = []
    for line in lines:
        tagged_words = [NUM_TAG if isNumber(word) else (URL_TAG if isURL(word) else word) for word in line.split()]
        tagged_lines.append(' '.join(tagged_words))
    
    with open (outputFile, "w") as fout:
        fout.write('\n'.join(tagged_lines))

def isNumber (word):
    return True if REGEX_NUM.match(word) else False

def isURL (word):
    return True if REGEX_URL.match(word) else False

def decodeBTaggerLemmaTags (inFileName, outFileName):
    
    inFile = codecs.open(inFileName,'r','utf-8')
    outFile = codecs.open(outFileName,'w','utf-8')
    
    for line in inFile:
        words = line.split(' ')
        if len(words) == 3:
            word = words[0]
            tag = words[-1][0:-1]
            if "@*@" in tag:
                prefix_split = tag.split("@*@")
                prefixparts = prefix_split[0].split("#")
                prefix_remove = prefixparts[0][1:]
                prefix_add = prefixparts[1]
                word = word[int(prefix_remove):]
                if len(prefix_add) >= 1:
                    word = prefix_add + word
                tag = prefix_split[-1]
            tagparts = tag.split("+")
            tag_remove = tagparts[0]
            tag_add = tagparts[1]
            if int(tag_remove) <= len(word):
                word = word[0:len(word)-int(tag_remove)]
                if len(tagparts[1]) >= 1:
                    word = word + tag_add
            outFile.write(words[0] + '\t' + words[1] + '\t' + word)
            outFile.write('\n')
        
        if line == '\n':
            outFile.write('\n')
            
    inFile.close()
    outFile.close()

def filter_btagger(word):
    original, POS, lemma = word.split('\t')
    if isNumber(lemma):
        return NUM_TAG
    elif isURL(lemma):
        return URL_TAG
    elif POS == "#":
        return ""
    else:
        return lemma

def filter_reldi(word):
    original, POS, lemma = word.split('\t')
    if isNumber(lemma):
        return NUM_TAG
    elif isURL (lemma):
        return URL_TAG
    elif POS == "Z":
        return ""
    else:
        return lemma
    
def filter_cst(word):
    original, lemma, POS = word.split('\t')
    if isNumber(lemma):
        return NUM_TAG
    elif isURL (lemma):
        return URL_TAG
    elif POS == "Z":
        return ""
    else:
        return lemma
    
def parseDecodedLemmas (decodedLemmas, outputFile, filter_function):
    
    with open (decodedLemmas, "r") as fin:
        decoded = fin.read()
    
    fout = open(outputFile,"w")
    for line in decoded.split("\n\n"):
        words = line.splitlines()
        filtered_words = [filter_function(word) for word in words]
        fout.write(" ".join([filtered_word for filtered_word in filtered_words if filtered_word]))
        fout.write("\n")
    fout.close()        
