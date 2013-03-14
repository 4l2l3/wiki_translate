#!/usr/bin/python
import re

text_in = open("pages_in_wiki/oases",'r').read()
text_out = text_in

def stylings_replace( pattern, text_in, trac_style, redmine_style ):
	matches = pattern.findall(text_in)
	for match in matches:
		if(trac_style.count('\'')==3):	#bold
			nested_text = match[3:(len(match)-3)]
		elif(trac_style.count('\'')==2): #ital
			nested_text = match[2:(len(match)-2)]
		else:
			inner_pattern = re.compile('[^'+trac_style+']+')
			nested_text = inner_pattern.search(match).group()

		text_in = text_in.replace(match, (redmine_style+ nested_text +redmine_style) )
	return text_in

def do_stylings(text_in):
	#build a function that takes in a SRE pattern object [*_pattern], text_out, and replacement text otherwise i'll have 7 for loops here
	text_out = text_in
	print text_in
	bold_pattern = re.compile('\'{3}.+?\'{3}')#We'll be performing these staggeredly. Because bold requires more apostrophes, it will always take precedence and can never be mistaken for italics, which can consume apostrophes intended for bolding.
	text_out = stylings_replace(bold_pattern, text_out, "'''", "*")

	#Because Redmine's italics format uses underlines, I figured it would be best to prioritize removing TRAC's underlines first to prevent any sort of confusion.
	undl_pattern = re.compile('_{2}.+?_{2}')
	text_out = stylings_replace(undl_pattern, text_out, "__", "+")

	strk_pattern = re.compile('~~.+?~~') #needs to be done before subscript
	text_out = stylings_replace(strk_pattern, text_out, "~~", "-") 

	ital_pattern = re.compile('\'{2}.++\'{2}') #we're using the dot instead of an alphanumeric match since we have to allow nested stylings
	text_out = stylings_replace(ital_pattern, text_out, "''", "_")

	#superscript = ('\^.+\^')   Redmine uses same format, we can probably skip this step.
	subs_pattern = re.compile(',,.+?,,')	
	text_out = stylings_replace(subs_pattern, text_out, ",,", "~")

	mono_pattern = re.compile('(\{{3}.+?\}{3}|`.+`)')
	text_out = stylings_replace(mono_pattern, text_out, "`{}", "@")
	return text_out

print do_stylings(text_out)
