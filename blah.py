#!/usr/bin/python
import re

wiki_pages = ['ABySS', 'ACLs', 'ADS', 'Ab-Init', 'Ansys', 'ApacheNutch', 'AutoDock', 'Blast', 'CDBurning', 'CMAQ-4.5.1', 'CMAQ-4.6', 'CMAQ-4.7', 'Cadence', 'CamelCase', 'CirceConnect', 'CirceDataAccess', 'CirceDataManagement', 'CirceDesktop', 'CirceHardware', 'CirceLayout', 'Cubit', 'DataBackup', 'DeveloperPortal', 'DevelopmentTools', 'Downtime2008', 'Downtime2009', 'ESPRIT', 'FAQ', 'FemlabUser', 'Fidap', 'GMT', 'GaussView', 'Gaussian', 'GibsonSpecs', 'GrADS', 'Grass', 'Gromacs', 'Gulp', 'HFSS', 'HPCPack2008R2Client', 'HPlatforms', 'Hadoop', 'HesiodConnect', 'IDLUser', 'InfiniBand', 'InterMapTxt', 'InterTrac', 'InterWiki', 'Iso2Mesh', 'JobRequirements', 'LAMMPS', 'MEGA', 'MM5', 'MM5OnIrce', 'MOVES', 'MPB', 'MPIBlast', 'MPP', 'MSModeling', 'MapleUser', 'MathemCluster', 'MathemUser', 'MatlabCluster', 'MatlabUser', 'Maya', 'Meep', 'Meme', 'Modules', 'MrBayes', 'MyriExp', 'NeedHPC', 'PGIInstall', 'PageTemplates', 'ParallelEnvironments', 'Quotas', 'RecentChanges', 'RestoreUtility', 'Rmpi', 'Run', 'SAS', 'SandBox', 'SoftPortalMockup', 'SoftwarePortal', 'SunblastData', 'Synopsys', 'TeraChem', 'TitleIndex', 'TracAccessibility', 'TracAdmin', 'TracBackup', 'TracBrowser', 'TracCgi', 'TracChangeset', 'TracEnvironment', 'TracFastCgi', 'TracFineGrainedPermissions', 'TracGuide', 'TracImport', 'TracIni', 'TracInstall', 'TracInterfaceCustomization', 'TracLinks', 'TracLogging', 'TracModPython', 'TracModWSGI', 'TracNavigation', 'TracNotification', 'TracPermissions', 'TracPlugins', 'TracQuery', 'TracReports', 'TracRepositoryAdmin', 'TracRevisionLog', 'TracRoadmap', 'TracRss', 'TracSearch', 'TracStandalone', 'TracSupport', 'TracSyntaxColoring', 'TracTickets', 'TracTicketsCustomFields', 'TracTimeline', 'TracUnicode', 'TracUpgrade', 'TracWiki', 'TracWorkflow', 'UsingComplexes', 'WEKA', 'Webdav', 'WhatIsHPC', 'WhatSoftware', 'WhoResources', 'WikiDeletePage', 'WikiFormatting', 'WikiHtml', 'WikiMacros', 'WikiNewPage', 'WikiPageNames', 'WikiProcessors', 'WikiRestructuredText', 'WikiRestructuredTextLinks', 'WikiStart', 'WinHPCJobStatus', 'WindowsISO', 'XWin32Install', 'XmingInstall', 'abinit', 'accountInfo', 'cp2k', 'dalton', 'desnex', 'devenv', 'dlpoly', 'dock6', 'esmf', 'fastxToolkit', 'fdtd', 'feram', 'gpuJobs', 'gridEngineInter', 'gridEngineIntro', 'gridEnginePolicy', 'gridEngineQueue', 'gridEngineRuntime', 'gridEngineStatus', 'gridEngineTechn', 'gridEngineUsers', 'here', 'jmol', 'libNuma', 'molden', 'namd', 'nwchem', 'oases', 'openfoam', 'openmm', 'proj', 'qe', 'siesta', 'testpage', 'titan2d', 'transabyss', 'vapor', 'vasp', 'velvet', 'vmd', 'vnc-class', 'vpnClient', 'websites', 'wrf']

text_in = open("links",'r').read()
text_out = text_in
#TRAC		mailto:someone@foo.bar
email_pat = re.compile('mailto:.+@[A-Za-z0-9.-]+\.[a-z]{2,}')
all_mailto = email_pat.findall(text_out)
for mailto in all_mailto:
	text_out = text_out.replace(mailto,mailto[len("mailto:"):])
	#REDMINE	someone@foo.bar

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
	if wiki_pages.count(word)!=0:#we're good and we link it
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
	new_twiki = "[["+page_name+"|"+title.group()+"]]"
	text_out = text_out.replace(twiki,new_twiki)
print text_out
