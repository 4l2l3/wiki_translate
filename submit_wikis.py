#!/usr/bin/python

import urllib, urllib2

wiki_pages = ['ABySS', 'ACLs', 'ADS', 'Ab-Init', 'Ansys', 'ApacheNutch', 'AutoDock', 'Blast', 'CDBurning', 'CMAQ-4.5.1', 'CMAQ-4.6', 'CMAQ-4.7', 'Cadence', 'CamelCase', 'CirceConnect', 'CirceDataAccess', 'CirceDataManagement', 'CirceDesktop', 'CirceHardware', 'CirceLayout', 'Cubit', 'DataBackup', 'DeveloperPortal', 'DevelopmentTools', 'Downtime2008', 'Downtime2009', 'ESPRIT', 'FAQ', 'FemlabUser', 'Fidap', 'GMT', 'GaussView', 'Gaussian', 'GibsonSpecs', 'GrADS', 'Grass', 'Gromacs', 'Gulp', 'HFSS', 'HPCPack2008R2Client', 'HPlatforms', 'Hadoop', 'HesiodConnect', 'IDLUser', 'InfiniBand', 'InterMapTxt', 'InterTrac', 'InterWiki', 'Iso2Mesh', 'JobRequirements', 'LAMMPS', 'MEGA', 'MM5', 'MM5OnIrce', 'MOVES', 'MPB', 'MPIBlast', 'MPP', 'MSModeling', 'MapleUser', 'MathemCluster', 'MathemUser', 'MatlabCluster', 'MatlabUser', 'Maya', 'Meep', 'Meme', 'Modules', 'MrBayes', 'MyriExp', 'NeedHPC', 'PGIInstall', 'PageTemplates', 'ParallelEnvironments', 'Quotas', 'RecentChanges', 'RestoreUtility', 'Rmpi', 'SAS', 'SandBox', 'SoftPortalMockup', 'SoftwarePortal', 'SunblastData', 'Synopsys', 'TeraChem', 'TitleIndex', 'TracAccessibility', 'TracAdmin', 'TracBackup', 'TracBrowser', 'TracCgi', 'TracChangeset', 'TracEnvironment', 'TracFastCgi', 'TracFineGrainedPermissions', 'TracGuide', 'TracImport', 'TracIni', 'TracInstall', 'TracInterfaceCustomization', 'TracLinks', 'TracLogging', 'TracModPython', 'TracModWSGI', 'TracNavigation', 'TracNotification', 'TracPermissions', 'TracPlugins', 'TracQuery', 'TracReports', 'TracRepositoryAdmin', 'TracRevisionLog', 'TracRoadmap', 'TracRss', 'TracSearch', 'TracStandalone', 'TracSupport', 'TracSyntaxColoring', 'TracTickets', 'TracTicketsCustomFields', 'TracTimeline', 'TracUnicode', 'TracUpgrade', 'TracWiki', 'TracWorkflow', 'UsingComplexes', 'WEKA', 'Webdav', 'WhatIsHPC', 'WhatSoftware', 'WhoResources', 'WikiDeletePage', 'WikiFormatting', 'WikiHtml', 'WikiMacros', 'WikiNewPage', 'WikiPageNames', 'WikiProcessors', 'WikiRestructuredText', 'WikiRestructuredTextLinks', 'WikiStart', 'WinHPCJobStatus', 'WindowsISO', 'XWin32Install', 'XmingInstall', 'abinit', 'accountInfo', 'cp2k', 'dalton', 'desnex', 'devenv', 'dlpoly', 'dock6', 'esmf', 'fastxToolkit', 'fdtd', 'feram', 'gpuJobs', 'gridEngineInter', 'gridEngineIntro', 'gridEnginePolicy', 'gridEngineQueue', 'gridEngineRuntime', 'gridEngineStatus', 'gridEngineTechn', 'gridEngineUsers', 'jmol', 'libNuma', 'molden', 'namd', 'nwchem', 'oases', 'openfoam', 'openmm', 'proj', 'qe', 'siesta', 'testpage', 'titan2d', 'transabyss', 'vapor', 'vasp', 'velvet', 'vmd', 'vnc-class', 'vpnClient', 'websites', 'wrf', 'Run', 'here']

dev_url = "https://cwa-dev.rc.usf.edu/projects/research-computing/wiki/"
suffix = "?parent=Applications"


for page_name in wiki_pages:
	app_file = open('pages_in_wiki/'+page_name,'r')
	wiki_markup = app_file.read()
	full_url = dev_url + page_name + suffix

	params = urllib.urlencode({'wiki_form':wiki_markup})
	req = urllib2.Request(full_url, params)
	req.add_header()
	rep = urllib2.urlopen(req)
	
