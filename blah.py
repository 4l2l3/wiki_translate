#!/usr/bin/python
import re

text_in = open("test_cases/paragraphs_code",'r').read()
text_out = text_in

#TRAC		{{{\n#!language\ncode\n}}}
#REDMINE	<pre><code class="language">\ncode\n</code></pre>
code_pat = re.compile('\{{3}\n#!.+\n[^}]+\n\}{3}')
code_blocks = code_pat.findall(text_out)
for block in code_blocks:
	lang = re.compile('\n#!.+\n').search(block).group().strip("\n")[2:]
	code = block[len("{{{\n#!")+len(lang)+len('\n') : len(block)-3]
	text_out = text_out.replace(block,'<pre><code class="'+lang+'">\n'+code+'</code></pre>')
print text_out
