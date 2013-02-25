#!/usr/bin/python

import re

def do_headers(text_in):
	#We're going to handle each header individually then once we have a list of original/TRAC headers and new/Redmine headers, we'll use re.sub('r...) to replace the old with the new.

	whole_header_pattern = re.compile('^(=+) [\w]+ (=+)$') #TODO: modify this regex to make sure starts(^) and ends($) the line 
	all_headers = whole_header_pattern.findall(text_in)
	
	header_text = re.compile('[\w\s]+') #we'll use this to extract header text
	count_eq = re.compile('=+') #we'll use this to count equal signs

	for header in all_headers:
		cur_hd_txt = header_text.search(header) #should only be one set of text per header
		#verify there was a match
		cur_eq_list = count_eq.findall(header)
		#verify they're of same length, else, syntax error from input :(
		eq_num1 = len(cur_eq_list[0])
		eq_num2 = len(cur_eq_list[1])
		if eq_num1 != eq_num2:
			print "Equal signs don't match in current header: '"+header+"'"#throw error
			continue #just ignore current header, don't translate
		new_hd = "h"+str(eq_num1)+"."+cur_hd_txt.group() #this string should include spacing
#what is this?	whole_header_pattern.finditer(text_in)
	text_out=""
	return text_out

def do_stylings(text_in):
	text_out=""
	return text_out

def do_paragraph_formatting(text_in):
	text_out=""
	return text_out

def do_links(text_in):
	text_out=""
	return text_out

def do_images(text_in):
	text_out=""
	return text_out

def do_misc(text_in):
	text_out=""
	return text_out

def translate(trac_text):
	trac_text = do_headers(trac_text)
	trac_text = do_stylings(trac_text)
	trac_text = do_paragraph_formatting(trac_text)
	trac_text = do_links(trac_text)
	trac_text = do_images(trac_text)
	trac_text = do_misc(trac_text)
	return trac_text

file_loc = "default"
while (file_loc!="no file"):
	#Get file contents
	print "Enter file location or 'no file' to exit program."
	file_loc = raw_input()
	if file_loc=="no file":
		break
	else:
		input_file = open(file_loc,'r').read()

	#Translate from trac wikiformatting to redmine wiki formatting
	output_text = translate(input_file)

	#Put redmine version in new file <filename>.redmine
	output_file = open(file_loc+'.redmine','w')
	output_file.write(output_text)

print "Normal program termination."
