#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Created on 2017. 02. 16
Updated on 2017. 02. 16
To run this program, you need to do following things.
   - preparing each techniques
   - download Git reporitory :: use launcher_GitInflator.py
   - make bug repository :: use launcher_repoMaker.py
   - make summary information files :: use ExecuteTools/executor/Counting.py
'''

from datetime import datetime
import os
import subprocess

from commons import Previous, Subjects, VersionUtil
from repository import GitInflator

here = os.path.dirname(os.path.abspath(__file__))

class Launcher(object):
	'''
	IRBL Techniques Launcher class
	'''

	# ProgramNames = ['BugLocator',  'BRTracer', 'BLUiR', 'AmaLgam',  'BLIA', 'Locus']
	ProgramNames = ['BugLocator',  'BLUiR', 'AmaLgam',  'BLIA', 'Locus']
	root = os.path.join(here, '..')
	ProgramPATH = os.path.join(root, 'techniques/')
	OutputPATH = os.path.join(root, 'expresults/')
	JavaOptions = '-Xms512m -Xmx4000m'
	JavaOptions_Locus = '-Xms3G -Xmx3G'
	TYPE = 'Test'

	def __init__(self):
		self.S = Subjects()
		if not os.path.exists(os.path.join(self.ProgramPATH, 'logs')):
			os.makedirs(os.path.join(self.ProgramPATH, 'logs'))

		t = datetime.now()
		timestr = t.strftime('%y%m%d_%H%M')
		self.logFileName = 'logs_%s'%timestr + '_%s.txt'

	def finalize(self):
		self.log.close()

	def createArguments(self, _params):
		if isinstance(_params, str):
			return _params
		if isinstance(_params, bytes):
			return _params.decode()

		paramsText = ''
		for key, value in _params.items():
			if key == 'v':
				if value is True:
					paramsText += ' -v'
			else:
				if value is None or value == '':
					continue
				paramsText += ' -%s %s' % (key, value)
		return paramsText

	def executeJava(self, _program, _params, _cwd=None, _project=None, _vname=None):
		if _cwd is None:
			_cwd = self.ProgramPATH

		options = self.JavaOptions if _program != 'Locus' else self.JavaOptions_Locus
		command = 'java %s -jar %s%s.jar %s' % (options, self.ProgramPATH, _program, self.createArguments(_params))
		commands = command.split(' ')

		t = datetime.now()
		timestr = t.strftime('Strat:%Y/%m/%d %H:%M')
		print('\n\n[%s]\nCMD:: %s' % (timestr, command))
		self.log.write('\n\n[%s]\nCMD:: %s\n' % (timestr, command))

		if _program == 'BLIA':
			self.log.write('working with %s / %s\n' % ( _project, _vname))
		try:
			#subprocess.call(commands, cwd=_cwd, shell=False) #, stdout=self.log, stderr=self.log)
			p = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, cwd=_cwd, text=True)
			while True:
				line = p.stdout.readline()
				if line == '':
					break
				# the real code does filtering here
				print(line.rstrip())
				self.log.write(line.rstrip()+'\n')
				self.log.flush()

		except Exception as e:
			print(e)
			return None
		return 'Success'

	def get_params(self, _program, _group, _project, _alpha, _version=None, _isUnion=False, _useMerge=False):
		bugrepo = self.S.getPath_bugrepo(_group, _project)
		params = {
			'n': '%s_%s' % (_project, _version if _isUnion is False else 'all'),
			's': self.S.getPath_source(_group, _project, _version) if _isUnion is False else self.S.getPath_gitrepo(_group, _project),  # source path
			'b': os.path.join(bugrepo,'repository%s.xml' % ('/%s' % _version if _isUnion is False else '')),  # base bug path
			'w': os.path.join(self.OutputPATH, self.TYPE, _group, _project) + '/',  # result path
			'a': _alpha,  # alpha parameter
		}

		if _useMerge:
			params['b'] = os.path.join(bugrepo,'repository_merge%s.xml' % ('/%s' % _version if _isUnion is False else ''))

		if _program in ['AmaLgam', 'BLIA', 'Locus']:
			params['g'] = self.S.getPath_gitrepo(_group, _project)  # git repo.

		if _program == 'BLIA':
			params = self.save_BLIA_config(_project, params, _version if not _isUnion else 'all')

		if _program == 'Locus':
			params = self.save_Locus_config(_project, params, _version if not _isUnion else 'all')

		return params

	def get_paramsDist(self, _program, _group, _project, _alpha, _version, _codeVersion):
		params = {
			'n': '%s_%s' % (_project, 'all'),
			's': self.S.getPath_source(_group, _project, _codeVersion),  # source path
			'b': os.path.join(self.S.getPath_bugrepo(_group, _project),'repository/%s.xml' % _version),  # base bug path
			'w': os.path.join(self.OutputPATH, self.TYPE, _group, _project)+'/',  # result path
			'a': _alpha,  # alpha parameter
		}
		if _program in ['AmaLgam', 'BLIA', 'Locus']:
			params['g'] = self.S.getPath_gitrepo(_group, _project)  # git repo.

		path = os.path.join(params['w'], '%s_%s'%(_program, params['n']))
		if os.path.exists(path) is True:
			for file in os.listdir(path):
				if file == 'revisions': continue
				if file == 'bugText': continue
				if file == 'hunkCode.txt': continue
				if file == 'hunkLog.txt': continue
				if file == 'hunkIndex.txt': continue
				if file == 'hunkCLTIndex.txt': continue
				if file == 'commitCLTINdex.txt': continue
				if file == 'sourceHunkLink.txt': continue
				if file == 'logOneline.txt': continue
				if file == 'concernedCommits.txt': continue
				os.remove(os.path.join(path, file))

		if _program == 'BLIA':
			params = self.save_BLIA_config(_project, params, _version)

		if _program == 'Locus':
			params = self.save_Locus_config(_project, params, 'all', _isAppend=True)

		return params

	def get_paramsOLD(self, _program, _group, _project, _alpha, _version):
		params = {
			'n': '%s_all' % _project,
			's': self.S.getPath_source(_group, _project, _version),  # source path
			'b': os.path.join(self.S.getPath_bugrepo(_group, _project), 'repository.xml'),  # base bug path
			'w': os.path.join(self.OutputPATH, self.TYPE, _group, _project)+'/',  # result path
			'a': _alpha,  # alpha parameter
		}
		if _program in ['AmaLgam', 'BLIA', 'Locus']:
			params['g'] = self.S.getPath_gitrepo(_group, _project)  # git repo.

		if (_program == 'BLIA' and _project not in ['PDE', 'JDT']) or (_program == 'Locus' and _project == 'AspectJ'):
			params['b'] = os.path.join(self.S.getPath_bugrepo(_group, _project), '%s_repository.xml' % _program)
		else:
			params['b'] = os.path.join(self.S.getPath_bugrepo(_group, _project), 'repository.xml')

		if _program == 'BLIA':
			params = self.save_BLIA_config(_project, params, 'all')

		if _program == 'Locus':
			params = self.save_Locus_config(_project, params, 'all')

		return params

	def save_BLIA_config(self, _project, _params, _versionName):
		alpha = 0.2
		beta = 0.2
		pastDays = 15

		filename = os.path.join(self.ProgramPATH, 'blia_properties', '%s.properties' % _project)
		with open(filename, 'w') as f:
			print('#Target product to run BLIA', file=f)
			print('TARGET_PRODUCT=' + _project, file=f)
			print('', file=f)
			print('# Execution configurations', file=f)
			print('WORK_DIR=' + _params['w'], file=f)
			print('THREAD_COUNT=10', file=f)
			print('', file=f)
			print('# For ' + _project, file=f)
			print('PRODUCT=' + _project, file=f)
			print('VERSION=' + _versionName, file=f)
			print('SOURCE_DIR=' + _params['s'], file=f)
			print('ALPHA=' + str(alpha), file=f)
			print('BETA=' + str(beta), file=f)
			print('PAST_DAYS=' + str(pastDays), file=f)
			print('REPO_DIR=' + _params['g'] + '/.git', file=f)
			print('BUG_REPO_FILE=' + _params['b'], file=f)
			print('COMMIT_SINCE=1990-04-01', file=f)
			print('COMMIT_UNTIL=2016-11-30', file=f)
			print('CANDIDATE_LIMIT_RATE=0.1', file=f)

		return filename

	def save_Locus_config(self, _project, _params, _versionName, _isAppend=False):
		filename = os.path.join(self.ProgramPATH, 'locus_properties', '%s_config.txt' % _versionName)
		with open(filename, 'w') as f:
			print('task=fileall', file=f)
			print('Project=' + _project, file=f)
			print('Version=' + _versionName, file=f)
			if _isAppend:
				print('MODE=append', file=f)
			print('repoDir=' + _params['g'], file=f)
			print('sourceDir=' + _params['s'], file=f)
			print('workingLoc='+ _params['w'], file=f)
			print('bugReport=' + _params['b'], file=f)
			print('changeOracle='+_params['w'], file=f)

		return filename

	def run(self, _type, _sGroup=None, _sProject=None,  _sProgram=None, _sVersion=None, _isUnion=False, _isDist=False, _useMerge=False):
		self.TYPE = _type
		nameTag = self.TYPE + ('_%s'%_sGroup if _sGroup is not None else '') + ('_%s'%_sProject if _sProject is not None else '') + ('_%s'%_sVersion if _sVersion is not None else '') + ('_%s'%_sProgram if _sProgram is not None else '')
		self.log = open(os.path.join(self.ProgramPATH, 'logs', self.logFileName%(nameTag)), 'w')

		# select target subjects or select all.
		for program in (self.ProgramNames if _sProgram is None else [_sProgram]):
			for group in (self.S.groups if _sGroup is None else [_sGroup]):
				for project in (self.S.projects[group] if _sProject is None else [_sProject]):
					#working selected subject and program.
					versions = self.S.bugs[project].keys()
					if _isDist is True:
						codeVersion = VersionUtil.get_latest_version(self.S.bugs[project].keys())
						for verName in (versions if _sVersion is None else [_sVersion]):
							if verName == 'all': continue
							params = self.get_paramsDist(program, group, project, 0.2, verName, codeVersion)
							self.executeJava(program+'_dist', params, _project=project, _vname =verName)

					elif _isUnion is True:
						# if the self.S.version[project] uses, the error occurs because there are versions with no bug report
						tagName = VersionUtil.get_latest_tag(self.S.versions[project])
						verName = VersionUtil.get_latest_version(self.S.bugs[project].keys())

						# check out target version
						print(' checkout %s... ' % tagName, end='')
						inf = GitInflator(project, self.S.urls[project], self.S.getPath_base(group, project))
						if inf.checkout(tagName) is False:
							print('Failed')
							continue
						print('Done')

						# execute JAVA
						params = self.get_params(program, group, project, 0.2, None, _isUnion)
						self.executeJava(program, params, _project=project, _vname =verName)
					else:
						# In the version is not single case,
						for verName in (versions if _sVersion is None else [_sVersion]):
							if verName == 'all': continue
							if _useMerge is True:
								if verName not in self.S.answers_merge[project]: continue
							# if the self.S.version[project] uses, the error occurs because there are versions with no bug report
							outputFile = os.path.join(self.OutputPATH, _type, group, project, '%s_%s_%s_output.txt'%(program, project, verName))
							# if os.path.exists(outputFile) is True:
							# 	print('Already exists :: %s '% outputFile)
							# 	continue
							params = self.get_params(program, group, project, 0.2, verName, _isUnion, _useMerge)
							self.executeJava(program, params, _project=project, _vname =verName)
						# for version
				# for program
			# for project
		#for group
		t = datetime.now()
		timestr = t.strftime('Done:%Y/%m/%d %H:%M')
		print('\n\n[%s]' % timestr)
		self.log.write('\n\n[%s]' % timestr)

	def runOLD(self, _type, _sGroup=None, _sProject=None, _sProgram=None):
		self.TYPE = _type
		nameTag = self.TYPE + ('_%s' % _sGroup if _sGroup is not None else '') + ('_%s' % _sProject if _sProject is not None else '')
		self.log = open(os.path.join(self.ProgramPATH, 'logs', self.logFileName%nameTag), 'w')

		self.S = Previous()
		for program in self.ProgramNames:
			if _sProgram is not None and program != _sProgram: continue

			for group in self.S.groups:
				if _sGroup is not None and group != _sGroup: continue

				for project in self.S.projects[group]:
					if _sProject is not None and project != _sProject: continue

					maxVersion = self.S.get_max_versions(program, project)
					versionName = '%s_%s' % (project, VersionUtil.get_versionName(maxVersion))
					alpha = 0.2 if not (program == 'BugLocator' and project == 'AspectJ') else 0.3
					params = self.get_paramsOLD(program, group, project, alpha, versionName)

					#print('java %s -jar %s%s.jar ' % (self.JavaOptions, self.ProgramPATH, program) + self.createArguments(params))
					self.executeJava(program, params, _project=project, _vname =versionName)

		t = datetime.now()
		timestr = t.strftime('Done:%Y/%m/%d %H:%M')
		print('\n\n[%s]' % timestr)
		self.log.write('\n\n[%s]' % timestr)

def getargs():
	import argparse
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('-p', dest='project', default=None, help='A specific project name what you want to work.')
	parser.add_argument('-g', dest='group', default=None, help='A specific group name what you want to work.')
	parser.add_argument('-t', dest='technique', default=None, help='A specific technique name what you want to work.')
	parser.add_argument('-v', dest='version', default=None, help='A specific version name what you want to work.')
	parser.add_argument('-w', dest='workType', default=None, help='workType : PreviousData or not. other case is NewData')
	parser.add_argument('-s', dest='isSingle', default=False, action='store_true', help='use latest source code for all bug report')
	parser.add_argument('-d', dest='isDist', default=False, action='store_true', help='use the multiple bug repository and the single source code')
	parser.add_argument('-m', dest='useMerge', default=False, action='store_true', help='use merged bug reporitory')

	args = parser.parse_args()

	if args.workType is None:
		parser.print_help()
		return None
	return args

if __name__ == '__main__':
	args = getargs()
	if args is None:
		exit(1)

	obj = Launcher()
	if args.workType.startswith('PreviousData'):
		obj.runOLD(args.workType, _sGroup=args.group, _sProject=args.project, _sProgram=args.technique)
	else:
		obj.run(args.workType, _sGroup=args.group, _sProject=args.project, _sVersion=args.version,
				_sProgram=args.technique, _isUnion=args.isSingle, _isDist=args.isDist, _useMerge = args.useMerge)

	obj.finalize()
