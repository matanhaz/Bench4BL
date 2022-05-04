# -*- coding: utf-8 -*-


import shutil
import os, stat
import subprocess
import time

from commons import VersionUtil

class GitInflator():
	workDir = ''       #'/home/user/bug/Apache/CAMEL/'
	projectName = ''   #'CAMEL'
	sourcesPath = ''    #'/home/user/bug/Apache/CAMEL/sources/'
	gitRepo = 'gitrepo'
	sourcesRepo = 'sources'
	projectPath = ''

	def __init__(self, _project, _basePATH):
		self.projectName = _project
		self.workDir = _basePATH
		self.sourcesPath = os.path.join(_basePATH, self.sourcesRepo)
		self.projectPath = os.path.join(self.workDir, self.gitRepo)
		
		self.gitURL = 'https://github.com/apache/commons-codec.git'
		
		pass

	def inflate(self, _versions):
		if _versions is None:
			return None

		self.projectPath = self.clone(True)
		print('Git Repo: %s'%self.projectPath)
		time.sleep(2)

		#check output path
		if os.path.exists(self.sourcesPath) is False:
			os.makedirs(self.sourcesPath)

		#get tags
		# tags = self.get_tags()
		# if tags is None: return False

		#print(self.projectName + ':: the number of tags are ' + str(len(tags)))
		size = len(_versions)
		count = 0
		for version, tag in _versions.items():
			vname = VersionUtil.get_versionName(version, self.projectName)
			count += 1
			print ('%s(%d/%d) :: [%s]'%(self.projectName, count, size, vname), end='')

			dest = os.path.join(self.sourcesPath, vname)
			if os.path.exists(dest) is True:
				print('  already exists!')
				continue

			tag = tag.strip()
			if tag == '':
				print ('invalidate tag name: "%s"'%tag)
				continue

			print(' checkout %s... ' %tag, end='')
			if self.checkout(tag) is False:
				print('Failed')
				continue
			time.sleep(2)

			#copy
			dest = os.path.join(self.sourcesPath, vname)
			print('  copy...', end='')
			if self.makecopy(dest) is False:
				print ('Failed!')
				continue
			print('Done')
			time.sleep(2)
		print('All checkout works done!!')
		pass

	#Delect alternative function when an error occured
	def del_rw(self, action, name, exc):
		os.chmod(name, stat.S_IWRITE)
		os.remove(name)

	def clone(self, passExists):
		basepath = os.path.join(self.workDir, self.gitRepo)
		if os.path.exists(basepath) is True:
			if passExists is True:
				return basepath
			shutil.rmtree(basepath, onerror=self.del_rw)

		try:
			subprocess.check_output(['git', 'clone', 'https://github.com/apache/commons-csv.git', self.gitRepo], cwd=self.workDir)
		except Exception as e:
			print(e)
			return None
		return basepath

	def get_tags(self):
		result = subprocess.check_output(['git', 'tag'], cwd=self.projectPath)
		if result is None:
			return None
		tags = result.decode().split('\n')
		return tags

	def checkout(self, _tag):
		flag = False

		# checkout tag
		while True:
			try:
				result = subprocess.check_output(['git', 'checkout', _tag], stderr=subprocess.STDOUT, cwd=self.projectPath)
			except Exception as e:
				print(e)
				self.clone(False)
				continue
			break

		# checkout validation
		result = subprocess.check_output(['git', 'branch'], cwd=self.projectPath)
		first = result.decode().split('\n')[0]
		if len(first) > 19:
			version = first[19:-1]
			if version.strip() == _tag:
				flag = True
		return flag

	def makecopy(self, _dest):
		# create target directory
		if not (_dest[-1:]=='\\' or _dest[-1:]=='/'):
			_dest += os.path.sep

		# remove previous info
		if os.path.exists(_dest):
			shutil.rmtree(_dest, onerror=self.del_rw)
		os.makedirs(_dest)

		#copy
		for filename in os.listdir(self.projectPath):
			if filename == '.git': continue
			fname = os.path.join(self.projectPath, filename)
			if os.path.isdir(fname) is True:
				shutil.copytree(fname, os.path.join(_dest,filename), symlinks=False, ignore=None)
			else:
				shutil.copy(fname, os.path.join(_dest,filename))
		return True
