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

	bold_pattern = re.compile('\'{3}.+?\'{3}')#We'll be performing these staggeredly. Because bold requires more apostrophes, it will always take precedence and can never be mistaken for italics, which can consume apostrophes intended for bolding.
	text_out = stylings_replace(bold_pattern, text_out, "'''", "*")

	#Because Redmine's italics format uses underlines, I figured it would be best to prioritize removing TRAC's underlines first to prevent any sort of confusion.
	undl_pattern = re.compile('_{2}.+?_{2}')
	text_out = stylings_replace(undl_pattern, text_out, "__", "+")

	strk_pattern = re.compile('~~.+?~~') #needs to be done before subscript
	text_out = stylings_replace(strk_pattern, text_out, "~~", "-") 

	ital_pattern = re.compile('\'{2}.+?\'{2}') #we're using the dot instead of an alphanumeric match since we have to allow nested stylings
	text_out = stylings_replace(ital_pattern, text_out, "''", "_")

	#superscript = ('\^.+\^')   Redmine uses same format, we can probably skip this step.
	subs_pattern = re.compile(',,.+?,,')	
	text_out = stylings_replace(subs_pattern, text_out, ",,", "~")

	mono_pattern = re.compile('(\{{3}.+?\}{3}|`.+`)')
	text_out = stylings_replace(mono_pattern, text_out, "`{}", "@")

	return text_out

def do_paragraph_formatting(text_in):
	text_out = text_in

	#TRAC		{{{\n#!language\ncode\n}}}
	#REDMINE	<pre><code class="language">\ncode\n</code></pre>
	code_pat = re.compile('\{{3}\n#!.+\n[^}]+\n\}{3}')
	code_blocks = code_pat.findall(text_out)
	for block in code_blocks:
		lang = re.compile('\n#!.+\n').search(block).group().strip("\n")[2:]
		code = block[len("{{{\n#!")+len(lang)+len('\n') : len(block)-3]
		text_out = text_out.replace(block,'<pre><code class="'+lang+'">\n'+code+'</code></pre>')
	#TRAC		text of my paragraph
	#REDMINE	p. text of my paragraph
	par_noi = re.compile('\n[A-Z].+')
	pars_noi = par_noi.findall(text_out)
	for par in pars_noi:
		text_out = text_out.replace(par,'\np. '+par[1:]) 


	#TRAC		number of spaces then paragraph text begins
	#REDMINE	p((((((((. text       ##the left paren is equivalent to number of spaces
	par_pat = re.compile('\n +')
	pars = par_pat.findall(text_out)
	for x in range(len(pars)):
		par = par_pat.search(text_out) #this will keep the positioning the same
		hd = par.start()
		tl = par.end()
		num_of_spaces = par.group().count(' ')
		text_out = text_out[:hd+1]+"p"+"("*num_of_spaces+". "+text_out[tl:] #+1 for newline

	return text_out

def do_links(text_in):
	wiki_pages = ['ABySS', 'ACLs', 'ADS', 'Ab-Init', 'Ansys', 'ApacheNutch', 'AutoDock', 		'Blast', 'CDBurning', 'CMAQ-4.5.1', 'CMAQ-4.6', 'CMAQ-4.7', 'Cadence', 'CamelCase', 		'CirceConnect', 'CirceDataAccess', 'CirceDataManagement', 'CirceDesktop', 'CirceHardware', 		'CirceLayout', 'Cubit', 'DataBackup', 'DeveloperPortal', 'DevelopmentTools', 		'Downtime2008', 'Downtime2009', 'ESPRIT', 'FAQ', 'FemlabUser', 'Fidap', 'GMT', 'GaussView', 		'Gaussian', 'GibsonSpecs', 'GrADS', 'Grass', 'Gromacs', 'Gulp', 'HFSS', 	'HPCPack2008R2Client', 'HPlatforms', 'Hadoop', 'HesiodConnect', 'IDLUser', 'InfiniBand', 		'InterMapTxt', 'InterTrac', 'InterWiki', 'Iso2Mesh', 'JobRequirements', 'LAMMPS', 'MEGA', 		'MM5', 'MM5OnIrce', 'MOVES', 'MPB', 'MPIBlast', 'MPP', 'MSModeling', 'MapleUser', 		'MathemCluster', 'MathemUser', 'MatlabCluster', 'MatlabUser', 'Maya', 'Meep', 'Meme', 		'Modules', 'MrBayes', 'MyriExp', 'NeedHPC', 'PGIInstall', 'PageTemplates', 		'ParallelEnvironments', 'Quotas', 'RecentChanges', 'RestoreUtility', 'Rmpi', 'Run', 'SAS', 		'SandBox', 'SoftPortalMockup', 'SoftwarePortal', 'SunblastData', 'Synopsys', 'TeraChem', 		'TitleIndex', 'TracAccessibility', 'TracAdmin', 'TracBackup', 'TracBrowser', 'TracCgi', 	'TracChangeset', 'TracEnvironment', 'TracFastCgi', 'TracFineGrainedPermissions', 		'TracGuide', 'TracImport', 'TracIni', 'TracInstall', 'TracInterfaceCustomization', 		'TracLinks', 'TracLogging', 'TracModPython', 'TracModWSGI', 'TracNavigation', 		'TracNotification', 'TracPermissions', 'TracPlugins', 'TracQuery', 'TracReports', 		'TracRepositoryAdmin', 'TracRevisionLog', 'TracRoadmap', 'TracRss', 'TracSearch', 		'TracStandalone', 'TracSupport', 'TracSyntaxColoring', 'TracTickets', 		'TracTicketsCustomFields', 'TracTimeline', 'TracUnicode', 'TracUpgrade', 'TracWiki', 		'TracWorkflow', 'UsingComplexes', 'WEKA', 'Webdav', 'WhatIsHPC', 'WhatSoftware', 		'WhoResources', 'WikiDeletePage', 'WikiFormatting', 'WikiHtml', 'WikiMacros', 		'WikiNewPage', 'WikiPageNames', 'WikiProcessors', 'WikiRestructuredText', 		'WikiRestructuredTextLinks', 'WikiStart', 'WinHPCJobStatus', 'WindowsISO', 'XWin32Install', 		'XmingInstall', 'abinit', 'accountInfo', 'cp2k', 'dalton', 'desnex', 'devenv', 'dlpoly', 		'dock6', 'esmf', 'fastxToolkit', 'fdtd', 'feram', 'gpuJobs', 'gridEngineInter', 	'gridEngineIntro', 'gridEnginePolicy', 'gridEngineQueue', 'gridEngineRuntime', 		'gridEngineStatus', 'gridEngineTechn', 'gridEngineUsers', 'here', 'jmol', 'libNuma', 		'molden', 'namd', 'nwchem', 'oases', 'openfoam', 'openmm', 'proj', 'qe', 'siesta', 		'testpage', 'titan2d', 'transabyss', 'vapor', 'vasp', 'velvet', 'vmd', 'vnc-class', 		'vpnClient', 'websites', 'wrf']

	text_out = text_in

	#TRAC		[mailto:someone@foo.bar "Email someone"]
	mailto_pat = re.compile('\[mailto:.+@[A-Za-z0-9.-]+\.[a-z]{2,} ".+"\]')
	all_mailtos = mailto_pat.findall(text_out)
	for single in all_mailtos:
		email_someone = re.compile('".+"').search(single) #var name refers to quoted text
		hd = email_someone.start()
		tl = email_someone.end()

		email_addr = single[len("[mailto:"):hd-1] #instead of 8, I put in len(...) for clarity
		#REDMINE	"Email someone":mailto:someone@foo.bar
		new_mailto = email_someone.group()+":mailto:"+email_addr
		text_out = text_out.replace(single, new_mailto)

	#TRAC		mailto:someone@foo.bar
	email_pat = re.compile('mailto:.+@[A-Za-z0-9.-]+\.[a-z]{2,}')
	all_mailto = email_pat.findall(text_out)
	for mailto in all_mailto:
		text_out = text_out.replace(mailto,mailto[len("mailto:"):])
		#REDMINE	someone@foo.bar

	#TRAC		[http://whatever.com/ "Title"]
	titled_url = re.compile('\[https?://.{4,} ".+"\]') #went the lax route and allowed URLs and titles to be of any format
	all_turls = titled_url.findall(text_out)
	for turl in all_turls:
		title = re.compile('".+"').search(turl)
		hd = title.start()
		tl = title.end()
		url = turl[1:hd-1] #first one cuts off leading "["
		#REDMINE	"Title":http://whatever.com
		new_turl = title.group() + ":" + url
		text_out = text_out.replace(turl,new_turl)

	#TRAC		WikiPageName
	words = text_out.split() 
	for word in words:
		if wiki_pages.count(word):#we're good and we link it
			text_out = text_out.replace(word, "[["+ word +"]]")
	#REDMINE	[[WikiPageName]]

	#TRAC		[wiki:WikiPageName "Title"]
	titled_wiki = re.compile('\[wiki:[A-Za-z0-9.-]+ ".+"\]')
	all_twiki = titled_wiki.findall(text_out)
	for twiki in all_twiki:
		title = re.compile('".+"').search(twiki)
		hd = title.start()
		page_name = twiki[len("[wiki:"):hd-1]
		#REDMINE	[[WikiPageName|Title]]
		new_twiki = "[["+page_name+"|"+title.group()[1:len(title.group())-1]+"]]"
		text_out = text_out.replace(twiki,new_twiki)
	return text_out

def do_images(text_in):
	text_out = text_in
	#TRAC		[[Image(image_url)]]
	#REDMINE	!image_url! 
	#TRAC		[[Image(attached_image.png)]]	
	#REDMINE	!attached_image.png!	
	image_loc = re.compile('\[\[Image\([^, ]{4,}\)\]\]')
	images = image_loc.findall(text_out)
	for image in images:
		loc = image[len("[[Image("):len(image)-3]
		text_out = text_out.replace(image, "!"+loc+"!")

	#SPECIAL ATTRIBUTES
	img_r = re.compile('\[\[Image\([^, ]{4,}, .+\)\]\]')
	imgs = img_r.findall(text_out)

	for img in imgs:
		#search only finds first occurrence
		img_name = re.compile('[^, ]+').search(img[len("[[Image("):]).group()

		#slicing after "[[Image(name, ", +2 is for space and comma 
		prefix_num = len("[[Image(")+len(img_name) +2 

		#TRAC		[[Image(photo.jpg, align=right)]]
		#REDMINE	!>image_url! 
		if (img[prefix_num:len(img)-3] =="align=right" ):
			text_out = text_out.replace(img,"!>"+img_name+"!")
		#TRAC		[[Image(photo.jpg, alt='Image title')]]
		#REDMINE	!image_url(Image title)! displays an image with an alt/title attribute	
		elif ((img[prefix_num:prefix_num+4])=="alt="):
			alt_txt = img[ prefix_num+4 : len(img)-3]
			text_out = text_out.replace(img, "!"+img_name+"("+alt_txt+")!")

		#TRAC		[[Image(photo.jpg, 120px)]]               
		#REDMINE	!{width: 100%}attached_image.png!	
		elif (img[len(img)-5:len(img)-3]=="px"): 
			pixel_size = img[prefix_num:len(img)-5]
			text_out = text_out.replace(img, "!{width: "+pixel_size+"%}"+img_name+"!")

		elif (img[len(img)-4:len(img)-3]=="%"):
			pixel_size = img[prefix_num:len(img)-4]
			text_out = text_out.replace(img, "!{width: "+pixel_size+"px}"+img_name+"!")

		#TRAC		[[Image(photo.jpg, key=value)]]
		#REDMINE	!{key: value}attached_image.png!
		else: 	
			keypairs = re.compile('[A-Za-z]+=[^,\]\)]+').findall(img[prefix_num:])
			new_keypairs = []
			for keypair in keypairs:
				match = re.compile('[a-zA-Z]+=').search(keypair)
				hd = match.start()
				key = match.group()
				val = keypair[len(key):] #doing this in the middle also removes the '='
				key = key[:len(key)-1] #chop off '='
				new_keypair = key+": "+val
				new_keypairs.append(new_keypair)
			text_out = text_out.replace(img,"!{"+ ", ".join([str(x) for x in new_keypairs])+"}"+img_name+"!")
	return text_out

def do_lists_tables(text_in):
	text_out = text_in

	#TRAC		||TABLE1||TABLE2||
	#REDMINE	|TABLE1|TABLE2|
	text_out = text_out.replace("||","|")

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

def do_definitions(text_in):
	text_out = text_in
	#TRAC		term::\n  definition
	#REDMINE	*term*\n  definition
	defs = re.compile('[a-zA-Z]+::\n  [^\n]+').findall(text_out)
	for defn in defs:
		colon_pos = defn.index('::')
		text_out = text_out.replace(defn, "*"+defn[:colon_pos]+"*"+defn[colon_pos+2:])
	return text_out

def translate(trac_text):
	#this order is important to account for '{{{' (monospace/code) and indentation(paragraph/lists)
	trac_text = do_headers(trac_text)	
	trac_text = do_lists_tables(trac_text)
	trac_text = do_paragraph_formatting(trac_text) #no-indents not converted
	trac_text = do_stylings(trac_text)
	trac_text = do_links(trac_text)
	trac_text = do_images(trac_text) 
	trac_text = do_definitions(trac_text)
	return trac_text

page_file = open("pages",'r')

for line in page_file:
	file_loc = "pages_in_wiki/" + line.rstrip('\n')
	#Get file contents
	input_file = open(file_loc,'r').read()

	#Translate from trac wikiformatting to redmine wiki formatting
	output_text = translate(input_file)
	print output_text
	#Put redmine version in new file <filename>.redmine
	output_file = open(file_loc+'.redmine','w')
	output_file.write(output_text)

print "Normal program termination."
