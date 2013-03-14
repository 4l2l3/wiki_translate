#!/usr/bin/python
import re

text_in = open("pages_in_wiki/oases",'r').read()
text_out = text_in

def do_lists_tables(text_in):
	text_out = text_in

	#TRAC		any number of indents then * text
	#REDMINE	any number of *
	#e.g.		'  *'  == '***'
	list_pat = re.compile('\n *\* .+')
	lists = list_pat.findall(text_out)
	for line in lists:
		spc_n_asterisk = re.compile(' *\*').search(line[1:]).group()
		spcs = spc_n_asterisk[:len(spc_n_asterisk)-1]
		space_count = spcs.count(' ')
		list_item = line[space_count+2:] #the one removes the original asterisk
		redmine_line = '\n*'+('*'*space_count)+list_item
		text_out = text_out.replace(line, redmine_line)
	return text_out

print do_lists_tables(text_out)
