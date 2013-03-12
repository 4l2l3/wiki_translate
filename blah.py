#!/usr/bin/python
import re

text_in = open("test_cases/lists",'r').read()
text_out = text_in

#TRAC		any number of indents then * text
#REDMINE	any number of *
#e.g.		'  *'  == '***'
list_pat = re.compile('\n *\*+ .+')
lists = list_pat.findall(text_out)
for line in lists:
	space_count = line.count(' ')
	list_item = line[space_count+1:]
	redmine_line = '\n*'+('*'*space_count)+list_item
	text_out = text_out.replace(line, redmine_line)
	
#trac		1. item1
#		 a. item1.a
#		  i. item1.a.i
#		1. item2

#redmine	# item1
#		## item 1.1
#		# item2
#nlist_pat = re.compile('(\n[0-9]+\. [^\n]+\n( [a-z]\. [^\n]+\n(  [xivlcdm]+\. [^\n]+)?)?)+')

nlist_pat = re.compile(' *([0-9]+|[a-z]+)\. [a-z:\'( ]+\n')
nlists = nlist_pat.finditer(text_out)
for nlist in nlists:
	aline = nlist.group()
	prefix = re.compile(' *[^ ]+').search(aline).group()
	space_count = prefix.count(' ')
	list_text = aline[len(prefix):]
	redmine_nlist = '#'+('#'*space_count)+list_text
	text_out = text_out.replace(aline, redmine_nlist)
print text_out

