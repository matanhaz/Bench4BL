#-*- coding: utf-8 -*-
'''
Created on 2016. 11. 19
Updated on 2016. 01. 09
'''

import os
import sys
from functools import cmp_to_key

import codecs
from commons import VersionUtil
from repository.GitLog import GitLog
from repository.BugFilter import BugFilter
from repository.GitVersion import GitVersion
import shutil


class BugRepositoryMaker:
	'''
	'''
	__name__ = 'BugRepositoryMaker'
	ProjectName = ''
	duplicatePath = ''
	repositoryPath = ''
	git = None
	gitVersion = None
	bugFilter = None

	def __init__(self, _projectName, _srcbugPath, _gitPath, _output):
		self.__name__ = _projectName
		if os.path.exists(_output) is False:
			os.makedirs(_output)

		self.ProjectName = _projectName
		self.duplicatePath = os.path.join(_output, 'duplicates.json')
		self.repositoryPath = os.path.join(_output, 'repository')
		self.git = GitLog( _projectName, _gitPath, os.path.join(_output, '.git.log'))
		self.gitVersion = GitVersion(_projectName, _gitPath, os.path.join(_output, '.git_version.txt'))
		self.bugFilter = BugFilter(_projectName, os.path.join(_srcbugPath, 'bugs'))
		pass

	#######################################################################
	# Conert XML
	#######################################################################
	def convertText(self, _bug):
		'''
		Convert bug object to XML
		:param _bug:
		:return:
		'''
		format =  '\t<bug id="%s" opendate="%s" fixdate="%s" resolution="%s">\n'
		format += '\t\t<buginformation>\n'
		format += '\t\t\t<summary>%s</summary>\n'
		format += '\t\t\t<description>%s</description>\n'
		format += '\t\t\t<version>%s</version>\n'
		format += '\t\t\t<fixedVersion>%s</fixedVersion>\n'
		format += '\t\t\t<type>%s</type>\n'
		format += '\t\t</buginformation>\n'
		format += '\t\t<fixedFiles>\n%s\n\t\t</fixedFiles>\n'
		format += '%s'  #this section for links
		format += '\t</bug>\n'

		fixedfiles = '\n'.join(
			'\t\t\t<file type="'+ f['type'] +'">' + f['name'] + '</file>'
			for f in _bug['fixedFiles']
		)

		links = '\n'.join(
			'\t\t\t<link type="'+ link['type']
			+ '" description="'+ link['description'] +'">'
			+ link['id'][link['id'].rfind('-')+1:] + '</link>'
			for link in _bug['links']
		)
		if links !='':
			links = '\t\t<links>\n%s\n\t\t</links>\n'%links

		text = format% (_bug['id'][_bug['id'].rfind('-')+1:],
						_bug['opendate'].strftime('%Y-%m-%d %H:%M:%S'),
						_bug['fixdate'].strftime('%Y-%m-%d %H:%M:%S'),
						_bug['resolution'],
						_bug['summary'],
						_bug['description'],
						_bug['version'],
						_bug['fixVersion'],
						_bug['type'],
						fixedfiles,
		                links)
		return text

	def convertTextSimple(self, _bug):
		'''
		Convert bug object to XML (simply)
		:param _bug:
		:return:
		'''
		format =  '\t<bug id="%s" opendate="%s" fixdate="%s" resolution="%s">\n'
		format += '\t\t<buginformation>\n'
		format += '\t\t\t<summary>%s</summary>\n'
		format += '\t\t\t<version>%s</version>\n'
		format += '\t\t\t<fixedVersion>%s</fixedVersion>\n'
		format += '\t\t\t<type>%s</type>\n'
		format += '\t\t</buginformation>\n'
		format += '\t\t<fixedFiles>%s</fixedFiles>\n'
		format += '%s'  #this section for links
		format += '\t</bug>\n'

		fixedfiles = str(len(_bug['fixedFiles']))

		links = '\n'.join(
			'\t\t\t<link type="'+ link['type']
			+ '" description="'+ link['description'] +'">'
			+ link['id'][link['id'].rfind('-')+1:] + '</link>'
			for link in _bug['links']
		)
		if links !='':
			links = '\t\t<links>\n%s\n\t\t</links>\n'%links

		text = format% (_bug['id'][_bug['id'].rfind('-')+1:],
						_bug['opendate'].strftime('%Y-%m-%d %H:%M:%S'),
						_bug['fixdate'].strftime('%Y-%m-%d %H:%M:%S'),
						_bug['resolution'],
						_bug['summary'],
						_bug['version'],
						_bug['fixVersion'],
						_bug['type'],
						fixedfiles,
		                links)
		return text

	def outputXML(self, _items, _targetPath):
		#write XML File
		output = codecs.open(_targetPath, 'w', 'utf-8')
		output.write('<?xml version = "1.0" encoding = "UTF-8" ?>\n<bugrepository name="%s">\n'%self.ProjectName)
		for item in _items:
			output.write(self.convertText(item))
		output.write('</bugrepository>')
		output.flush()
		output.close()
		pass

	def printSample(self, _items):

		types = {}
		for item in _items:
			if item['type'] not in types:
				types[item['type']] = 1

		output = codecs.open(self.repositoryPath + '.type', 'w', 'utf-8')
		for t in types.keys():
			for item in _items:
				if item['type'] != t : continue
				output.write(self.convertText(item))
			output.write('\n\n<!-- -------------------------------------------------------------- -->\n\n')
		output.close()

		versions = {}
		for item in _items:
			if item['version'] not in versions:
				versions[item['version']] = 1

		output = codecs.open(self.repositoryPath + '.version', 'w', 'utf-8')
		for ver in versions.keys():
			for item in _items:
				if item['version'] != ver: continue
				output.write(self.convertTextSimple(item))
			output.write('\n\n<!-- -------------------------------------------------------------- -->\n\n')
		output.close()

	def getVersionString(self, _version):
		vname = self.ProjectName + '_' + _version.replace('.', '_')
		if vname.endswith('_') is True:
			vname = vname[:-1]
		return vname

	def getItemsByVersion(self, _items, _versions):
		# write XML File

		_versions = list(_versions)
		_versions.sort(key=cmp_to_key(VersionUtil.cmpVersion))
		version_bugs = dict((ver, list()) for ver in _versions)

		size = len(_versions)
		for idx in range(0, size):
			version = _versions[idx]
			nextVersion = _versions[idx + 1] if idx != size - 1 else '10000.0'  # assign big. version number

			for bugitem in _items:
				if VersionUtil.cmpVersion(version, bugitem['version']) > 0 and idx!=0: continue
				if VersionUtil.cmpVersion(bugitem['version'], nextVersion) >= 0: continue
				version_bugs[version].append(bugitem)

		return version_bugs

	def outputDuplicates(self, _dupgroups):
		output = codecs.open(self.duplicatePath, 'w', 'utf-8')
		output.write('{"%s":[\n' % self.ProjectName.lower())
		groupcnt  = 0
		for group in _dupgroups:
			groupcnt += 1
			srcID = int(group['src'][group['src'].find('-')+1:].strip())
			destID = int(group['dest'][group['dest'].find('-')+1:].strip())
			output.write('\t[%d, %d]'%(srcID, destID))
			if groupcnt != len(_dupgroups):
				output.write(',')
			if group['fixedboth'] is True:
				output.write(' # fixed both')
			output.write('\n')

		output.write(']}\n')
		output.close()
		return len(_dupgroups)

	def getItemsOnlyVersion(self, _items):
		newItems = []
		for item in _items:
			if VersionUtil.hasVersion(item['version']) is False: continue
			newItems.append(item)
		return newItems

	def filter_dupgroups(self, _dups, _bugs):
		bugIDset = set([item['id'] for item in _bugs])

		newDups = []
		for dup in _dups:
			if dup['src'] not in bugIDset or dup['dest'] not in bugIDset: continue
			newDups.append(dup)

		#change chaning bug::   A-> B -> C   ==>    A->C, B->C
		count = 1
		while count !=0:
			count = 0
			for dup in newDups:
				src = dup['src']
				for subdup in newDups:
					if subdup['dest'] != src: continue
					dup['src'] = subdup['src']
					count += 1
					break
		return newDups

	#######################################################################
	# Overall Process
	#######################################################################
	def run(self, _versions, _removeTest=True):

		print(('[%s] start making bug repositories for %s' %(self.__name__, self.ProjectName)))
		logs = self.git.load()
		tagmaps = self.gitVersion.load()
		items, dupgroups = self.bugFilter.run(logs, tagmaps, _removeTest)
		print(('[%s] %d Bug reports has been merged!' % (self.ProjectName, len(items))))

		# refine more
		FilteredItems = self.getItemsOnlyVersion(items)
		versionItems = self.getItemsByVersion(FilteredItems, _versions)
		print(('[%s] Making bug repository for each version...' % self.ProjectName))

		# revise dup bug reports which are not include removed items.
		# and remove missed bugs from FilteredItems when the version making
		dupgroups = self.filter_dupgroups(dupgroups, FilteredItems)
		print(('[%s] Filtered bug reports.' % self.ProjectName))

		#self.printSample(items)
		self.outputXML(items, self.repositoryPath + '_full.xml')
		self.outputXML(FilteredItems, self.repositoryPath + '.xml')

		if os.path.exists(self.repositoryPath) is True:
			shutil.rmtree(self.repositoryPath)
		if os.path.exists(self.repositoryPath) is False:
			os.makedirs(self.repositoryPath)

		exists = set([])
		for ver in versionItems.keys():
			if len(versionItems[ver])==0: continue
			exists.add(ver)
			outputPath = os.path.join(self.repositoryPath, self.getVersionString(ver) + '.xml')
			self.outputXML(versionItems[ver], outputPath)
		print('Done')

		exists = list(exists)
		exists.sort(key=cmp_to_key(VersionUtil.cmpVersion))
		print(('[%s] %d version repositories has been created! %s' % (self.ProjectName, len(exists), exists)))

		dupcnt = self.outputDuplicates(dupgroups)
		print(('[%s] %d duplicate bug-set has been created!' % (self.ProjectName, dupcnt)))
		pass

###############################################################################################################
###############################################################################################################
###############################################################################################################
def getargs():
	import argparse
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('-p', dest='project', help='project name')
	parser.add_argument('-g', dest='gitPath', help='git cloned path; we will extract log message from this.')
	parser.add_argument('-s', dest='bugPath', default=None, help='the directory contains bug reports')
	parser.add_argument('-v', dest='versions', default=None, help='versions')

	args = parser.parse_args()

	if args.project is None or args.gitPath is None or args.bugPath is None:
		parser.print_help()
		return None
	return args


if __name__ == "__main__":
	args = getargs()
	if args is None:
		# from collections import namedtuple
		# Args = namedtuple('Args', 'project gitPath bugPath versions')
		#args = Args('PDE', '/var/experiments/BugLocalization/dist/data/Previous/PDE/gitrepo/', '/var/experiments/BugLocalization/dist/data/Previous/PDE/bugrepo/PDE/', ['4.5'])

		exit(0)

	obj = BugRepositoryMaker(args.project, args.bugPath, args.gitPath, args.bugPath)
	obj.run(args.versions)
	pass
