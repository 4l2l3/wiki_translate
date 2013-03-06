#!/usr/bin/python

import re

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
	bold_pattern = re.compile('\'{3}.+\'{3}')#We'll be performing these staggeredly. Because bold requires more apostrophes, it will always take precedence and can never be mistaken for italics, which can consume apostrophes intended for bolding.
	text_out = stylings_replace(bold_pattern, text_out, "'''", "*")

	#Because Redmine's italics format uses underlines, I figured it would be best to prioritize removing TRAC's underlines first to prevent any sort of confusion.
	undl_pattern = re.compile('_{2}.+_{2}')
	text_out = stylings_replace(undl_pattern, text_out, "__", "+")

	strk_pattern = re.compile('~~.+~~') #needs to be done before subscript
	text_out = stylings_replace(strk_pattern, text_out, "~~", "-") 

	ital_pattern = re.compile('\'{2}.+\'{2}') #we're using the dot instead of an alphanumeric match since we have to allow nested stylings
	text_out = stylings_replace(ital_pattern, text_out, "''", "_")

	#superscript = ('\^.+\^')   Redmine uses same format, we can probably skip this step.
	subs_pattern = re.compile(',,.+,,')	
	text_out = stylings_replace(subs_pattern, text_out, ",,", "~")

	mono_pattern = re.compile('(\{{3}.+\}{3}|`.+`)')
	text_out = stylings_replace(mono_pattern, text_out, "`{}", "@")

	return text_out

def do_paragraph_formatting(text_in):
	text_out = text_in
	return text_out

def do_links(text_in):
	wiki_pages = ['ABySS', 'ACLs', 'ADS', 'Ab-Init', 'Ansys', 'ApacheNutch', 'AutoDock', 		'Blast', 'CDBurning', 'CMAQ-4.5.1', 'CMAQ-4.6', 'CMAQ-4.7', 'Cadence', 'CamelCase', 		'CirceConnect', 'CirceDataAccess', 'CirceDataManagement', 'CirceDesktop', 'CirceHardware', 		'CirceLayout', 'Cubit', 'DataBackup', 'DeveloperPortal', 'DevelopmentTools', 		'Downtime2008', 'Downtime2009', 'ESPRIT', 'FAQ', 'FemlabUser', 'Fidap', 'GMT', 'GaussView', 		'Gaussian', 'GibsonSpecs', 'GrADS', 'Grass', 'Gromacs', 'Gulp', 'HFSS', 	'HPCPack2008R2Client', 'HPlatforms', 'Hadoop', 'HesiodConnect', 'IDLUser', 'InfiniBand', 		'InterMapTxt', 'InterTrac', 'InterWiki', 'Iso2Mesh', 'JobRequirements', 'LAMMPS', 'MEGA', 		'MM5', 'MM5OnIrce', 'MOVES', 'MPB', 'MPIBlast', 'MPP', 'MSModeling', 'MapleUser', 		'MathemCluster', 'MathemUser', 'MatlabCluster', 'MatlabUser', 'Maya', 'Meep', 'Meme', 		'Modules', 'MrBayes', 'MyriExp', 'NeedHPC', 'PGIInstall', 'PageTemplates', 		'ParallelEnvironments', 'Quotas', 'RecentChanges', 'RestoreUtility', 'Rmpi', 'Run', 'SAS', 		'SandBox', 'SoftPortalMockup', 'SoftwarePortal', 'SunblastData', 'Synopsys', 'TeraChem', 		'TitleIndex', 'TracAccessibility', 'TracAdmin', 'TracBackup', 'TracBrowser', 'TracCgi', 	'TracChangeset', 'TracEnvironment', 'TracFastCgi', 'TracFineGrainedPermissions', 		'TracGuide', 'TracImport', 'TracIni', 'TracInstall', 'TracInterfaceCustomization', 		'TracLinks', 'TracLogging', 'TracModPython', 'TracModWSGI', 'TracNavigation', 		'TracNotification', 'TracPermissions', 'TracPlugins', 'TracQuery', 'TracReports', 		'TracRepositoryAdmin', 'TracRevisionLog', 'TracRoadmap', 'TracRss', 'TracSearch', 		'TracStandalone', 'TracSupport', 'TracSyntaxColoring', 'TracTickets', 		'TracTicketsCustomFields', 'TracTimeline', 'TracUnicode', 'TracUpgrade', 'TracWiki', 		'TracWorkflow', 'UsingComplexes', 'WEKA', 'Webdav', 'WhatIsHPC', 'WhatSoftware', 		'WhoResources', 'WikiDeletePage', 'WikiFormatting', 'WikiHtml', 'WikiMacros', 		'WikiNewPage', 'WikiPageNames', 'WikiProcessors', 'WikiRestructuredText', 		'WikiRestructuredTextLinks', 'WikiStart', 'WinHPCJobStatus', 'WindowsISO', 'XWin32Install', 		'XmingInstall', 'abinit', 'accountInfo', 'cp2k', 'dalton', 'desnex', 'devenv', 'dlpoly', 		'dock6', 'esmf', 'fastxToolkit', 'fdtd', 'feram', 'gpuJobs', 'gridEngineInter', 	'gridEngineIntro', 'gridEnginePolicy', 'gridEngineQueue', 'gridEngineRuntime', 		'gridEngineStatus', 'gridEngineTechn', 'gridEngineUsers', 'here', 'jmol', 'libNuma', 		'molden', 'namd', 'nwchem', 'oases', 'openfoam', 'openmm', 'proj', 'qe', 'siesta', 		'testpage', 'titan2d', 'transabyss', 'vapor', 'vasp', 'velvet', 'vmd', 'vnc-class', 		'vpnClient', 'websites', 'wrf']

	text_out = text_in
	return text_out

def do_images(text_in):
	text_out = text_in
	return text_out

def do_misc(text_in):
	text_out = text_in
	return text_out

def translate(trac_text):
	trac_text = do_headers(trac_text)
	trac_text = do_stylings(trac_text)
	trac_text = do_paragraph_formatting(trac_text)
	trac_text = do_links(trac_text)
	trac_text = do_images(trac_text)
	trac_text = do_misc(trac_text)
	return trac_text

print "Enter file location or 'no file' to exit program."
file_loc = raw_input()
while (file_loc!="no file"):
	#Get file contents
	input_file = open(file_loc,'r').read()

	#Translate from trac wikiformatting to redmine wiki formatting
	output_text = translate(input_file)

	#Put redmine version in new file <filename>.redmine
	output_file = open(file_loc+'.redmine','w')
	output_file.write(output_text)

	#Get next file or break loop
	print "Enter file location or 'no file' to exit program."
	file_loc = raw_input()

print "Normal program termination."
