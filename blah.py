#!/usr/bin/python
import re

wiki_pages = ['ABySS', 'ACLs', 'ADS', 'Ab-Init', 'Ansys', 'ApacheNutch', 'AutoDock', 'Blast', 'CDBurning', 'CMAQ-4.5.1', 'CMAQ-4.6', 'CMAQ-4.7', 'Cadence', 'CamelCase', 'CirceConnect', 'CirceDataAccess', 'CirceDataManagement', 'CirceDesktop', 'CirceHardware', 'CirceLayout', 'Cubit', 'DataBackup', 'DeveloperPortal', 'DevelopmentTools', 'Downtime2008', 'Downtime2009', 'ESPRIT', 'FAQ', 'FemlabUser', 'Fidap', 'GMT', 'GaussView', 'Gaussian', 'GibsonSpecs', 'GrADS', 'Grass', 'Gromacs', 'Gulp', 'HFSS', 'HPCPack2008R2Client', 'HPlatforms', 'Hadoop', 'HesiodConnect', 'IDLUser', 'InfiniBand', 'InterMapTxt', 'InterTrac', 'InterWiki', 'Iso2Mesh', 'JobRequirements', 'LAMMPS', 'MEGA', 'MM5', 'MM5OnIrce', 'MOVES', 'MPB', 'MPIBlast', 'MPP', 'MSModeling', 'MapleUser', 'MathemCluster', 'MathemUser', 'MatlabCluster', 'MatlabUser', 'Maya', 'Meep', 'Meme', 'Modules', 'MrBayes', 'MyriExp', 'NeedHPC', 'PGIInstall', 'PageTemplates', 'ParallelEnvironments', 'Quotas', 'RecentChanges', 'RestoreUtility', 'Rmpi', 'Run', 'SAS', 'SandBox', 'SoftPortalMockup', 'SoftwarePortal', 'SunblastData', 'Synopsys', 'TeraChem', 'TitleIndex', 'TracAccessibility', 'TracAdmin', 'TracBackup', 'TracBrowser', 'TracCgi', 'TracChangeset', 'TracEnvironment', 'TracFastCgi', 'TracFineGrainedPermissions', 'TracGuide', 'TracImport', 'TracIni', 'TracInstall', 'TracInterfaceCustomization', 'TracLinks', 'TracLogging', 'TracModPython', 'TracModWSGI', 'TracNavigation', 'TracNotification', 'TracPermissions', 'TracPlugins', 'TracQuery', 'TracReports', 'TracRepositoryAdmin', 'TracRevisionLog', 'TracRoadmap', 'TracRss', 'TracSearch', 'TracStandalone', 'TracSupport', 'TracSyntaxColoring', 'TracTickets', 'TracTicketsCustomFields', 'TracTimeline', 'TracUnicode', 'TracUpgrade', 'TracWiki', 'TracWorkflow', 'UsingComplexes', 'WEKA', 'Webdav', 'WhatIsHPC', 'WhatSoftware', 'WhoResources', 'WikiDeletePage', 'WikiFormatting', 'WikiHtml', 'WikiMacros', 'WikiNewPage', 'WikiPageNames', 'WikiProcessors', 'WikiRestructuredText', 'WikiRestructuredTextLinks', 'WikiStart', 'WinHPCJobStatus', 'WindowsISO', 'XWin32Install', 'XmingInstall', 'abinit', 'accountInfo', 'cp2k', 'dalton', 'desnex', 'devenv', 'dlpoly', 'dock6', 'esmf', 'fastxToolkit', 'fdtd', 'feram', 'gpuJobs', 'gridEngineInter', 'gridEngineIntro', 'gridEnginePolicy', 'gridEngineQueue', 'gridEngineRuntime', 'gridEngineStatus', 'gridEngineTechn', 'gridEngineUsers', 'here', 'jmol', 'libNuma', 'molden', 'namd', 'nwchem', 'oases', 'openfoam', 'openmm', 'proj', 'qe', 'siesta', 'testpage', 'titan2d', 'transabyss', 'vapor', 'vasp', 'velvet', 'vmd', 'vnc-class', 'vpnClient', 'websites', 'wrf']

text_in = open("wiki_translate/links",'r').read()
text_out = text_in

#TRAC		[mailto:someone@foo.bar "Email someone"]
mailto_pat = re.compile('\[mailto:[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[a-z]{2,} ".+"\]')
all_mailtos = mailto_pat.findall(text_out)
for single in all_mailtos:
	email_someone = re.compile('".+"').search(single)
	hd = email_someone.start()
	tl = email_someone.end()
	new_mailto = single[hd:tl]+":mailto:"+email_addr
	
	
#REDMINE	"Email someone":mailto:someone@foo.bar

#TRAC		[http://whatever.com/ "Title"]
titled_page = re.compile('\[https?://[a-zA-Z0-9./]{4,} "[A-Za-z0-9 ]+"\]')
#REDMINE	"Title":http://whatever.com

#TRAC		[wiki:WikiPageName "Title"]
titled_wiki = re.compile('\[wiki:[A-Za-z0-9 ]+ "[A-Za-z0-9 ]+"\]')
#REDMINE	[[WikiPageName|Title]]

#TRAC		WikiPageName
if wiki_pages.count(inputty)!=0:
	#we're good and we link it
#REDMINE	[[WikiPageName]]
print text_out
