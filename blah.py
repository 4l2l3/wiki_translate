#!/usr/bin/python
import re

def do_headers(text_in):
	text_out = text_in 

	whole_header_pattern = re.compile('=+ [^=\n]+ =+') #TODO: modify this regex to make sure starts(^) and ends($) the line?? Because python treats the entire file as one line, this match only works for single-line files. I've modified the regex to just use the trailing newline.
	all_headers = whole_header_pattern.finditer(text_out)
	
	header_text = re.compile('[\w\s]+') 
	count_eq = re.compile('=+') 

	for header in all_headers:
		cur_hd_txt = header_text.search(header.group()) #should only be one set of text per header
		cur_eq_list = count_eq.findall(header.group())
		eq_num1 = len(cur_eq_list[0])
		eq_num2 = len(cur_eq_list[1])
		if eq_num1 != eq_num2:
			print "Equal signs don't match in current header: '"+header+"'"#throw error
			continue #just ignore current header, don't translate
		new_hd = "h"+str(eq_num1)+"."+cur_hd_txt.group().rstrip()#rstrip gets rid of our trailing space
		#It appears there's a glitch with header.start(), it's matching '= header_text ===' instead of '=== header_text ===' and therefore .start() returns 2 spaces before our full match begins. Also does the same with 4 equal signs.
		#before = text_in[:(header.span()[0])]
		#after = text_in[(header.span()[1]):]
		#text_in = before+new_hd+after #replacing
		
		#The following line is a hacky band-aid for it.
		text_out = text_out.replace(header.group(),new_hd) 

	return text_out

text_in = open("pages_in_wiki/ABySS",'r').read()
text_out = text_in

print do_headers(text_out)
