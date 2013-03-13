#!/usr/bin/python
import re

page_file = open("pages",'r')

for line in page_file:
	print line.rstrip('\n')
