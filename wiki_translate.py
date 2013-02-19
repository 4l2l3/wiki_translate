#!/usr/bin/python

def do_headers(text_in):
	print "headers"
	text_out=""
	return text_out

def do_stylings(text_in):
	print "stylings"
	text_out=""
	return text_out

def do_paragraph_formatting(text_in):
	print "paragraphs"
	text_out=""
	return text_out

def do_links(text_in):
	print "links"
	text_out=""
	return text_out

def do_images(text_in):
	print "images"
	text_out=""
	return text_out

def do_misc(text_in):
	print "misc"
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

def get_file_loc():
	print "Enter file location or 'no file' to exit program."
	return raw_input()

file_loc = "default"
while (file_loc!="no file"):
	#Get file contents
	file_loc = get_file_loc()
	input_file = open(file_loc,'r').read()

	#Translate from trac wikiformatting to redmine wiki formatting
	output_text = translate(input_file)

	#Put redmine version in new file <filename>.redmine
	output_file = open(file_loc+'.redmine','w')
	output_file.write(output_text)

print "Normal program termination."
