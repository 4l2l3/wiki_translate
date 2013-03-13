#!/usr/bin/python
import re, sys
def do_headers(text_in):
	#We're going to handle each header individually then once we have a list of original/TRAC headers and new/Redmine headers, we'll use re.sub('r...) to replace the old with the new.
	text_out = text_in #just in-case, let's not destroy our original text_in

	whole_header_pattern = re.compile('(=+) [\w]+ (=+)\n') #TODO: modify this regex to make sure starts(^) and ends($) the line?? Because python treats the entire file as one line, this match only works for single-line files. I've modified the regex to just use the trailing newline.
	all_headers = whole_header_pattern.finditer(text_out)
	
	header_text = re.compile('[\w\s]+') #we'll use this to extract header text
	count_eq = re.compile('=+') #we'll use this to count equal signs

	for header in all_headers:
		cur_hd_txt = header_text.search(header.group()) #should only be one set of text per header
		#verify there was a match
		cur_eq_list = count_eq.findall(header.group())
		#verify they're of same length, else, syntax error from input :(
		eq_num1 = len(cur_eq_list[0])
		eq_num2 = len(cur_eq_list[1])
		if eq_num1 != eq_num2:
			print "Equal signs don't match in current header: '"+header+"'"#throw error
			continue #just ignore current header, don't translate
		new_hd = "h"+str(eq_num1)+"."+cur_hd_txt.group().rstrip()+"\n"#rstrip gets rid of our trailing space
		#It appears there's a glitch with header.start(), it's matching '= header_text ===' instead of '=== header_text ===' and therefore .start() returns 2 spaces before our full match begins. Also does the same with 4 equal signs.
		#before = text_in[:(header.span()[0])]
		#after = text_in[(header.span()[1]):]
		#text_in = before+new_hd+after #replacing
		
		#The following line is a hacky band-aid for it.
		text_out = text_out.replace(header.group(),new_hd) 

	return text_out
def do_lists_tables(text_in):
	text_out = text_in

	#TRAC		||TABLE1||TABLE2||
	#REDMINE	|TABLE1|TABLE2|
	text_out = text_out.replace("||","|")

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
	return text_out

def translate(trac_text):
	#this order is important to account for '{{{' (monospace/code) and indentation(paragraph/lists)
	trac_text = do_headers(trac_text)

	
	trac_text = do_lists_tables(trac_text)
#	trac_text = do_paragraph_formatting(trac_text)
#	trac_text = do_stylings(trac_text)
#	trac_text = do_links(trac_text)
#	trac_text = do_images(trac_text)
#	trac_text = do_definitions(trac_text)
	return trac_text

print "Enter file location or 'no file' to exit program."
file_loc = raw_input()
while (file_loc!="no file"):
	#Get file contents
	input_file = open(file_loc,'r').read()

	#Translate from trac wikiformatting to redmine wiki formatting
	output_text = translate(input_file)
	print output_text
	#Put redmine version in new file <filename>.redmine
	output_file = open(file_loc+'.redmine','w')
	output_file.write(output_text)

	#Get next file or break loop
	print "Enter file location or 'no file' to exit program."
	file_loc = raw_input()

print "Normal program termination."
