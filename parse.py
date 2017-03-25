import fileinput
import HTMLParser

column = 0
is_serbian = False
htmlParser = HTMLParser.HTMLParser()

for line in fileinput.input():
	if line.startswith('<p'):
		is_serbian = 'lang="sr"' in line
	elif line == '</p>':
		is_serbian = False
	elif is_serbian:
		if line == '<s>\n':
			sentence = []
		elif line == '</s>\n':
			if sentence:
				print " ".join(sentence).encode('utf-8')
		elif line.startswith('<'):
			pass
		else:
			sentence.append(htmlParser.unescape(line.split('\t')[column].decode('utf-8')))