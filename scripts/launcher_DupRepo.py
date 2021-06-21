#!/usr/bin/env python
#-*- coding: utf-8 -*-


import os
import shutil

from commons import Subjects
from repository import DupMergeRepositoryMaker

def clean(_sGroup=None, _sProject=None):
	S = Subjects()
	for group in S.groups:
		for project in S.projects[group]:
			print(('cleanning %s / %s ' % (group, project)))
			dirpath = os.path.join(S.getPath_bugrepo(group, project), 'repository_merge')
			fullrepo = os.path.join(S.getPath_bugrepo(group, project), 'repository_merge.xml')
			try:
				shutil.rmtree(dirpath)
			except Exception as e:
				print('Failed to remove repository folder')
			try:
				os.remove(fullrepo)
			except Exception as e:
				print('Failed to remove full repository file')

def work(_sGroup=None, _sProject=None):
	obj = DupMergeRepositoryMaker()
	S = Subjects()
	for group in self.S.groups:
		if _sGroup is None or group == _sGroup:
			for project in self.S.projects[group]:
				if _sProject is None or project == _sProject:
					obj.make(group, project)


def getargs():
	import argparse
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('-p', dest='project', default=None, help='A specific project name what you want to work.')
	parser.add_argument('-g', dest='group', default=None, help='A specific group name what you want to work.')
	parser.add_argument('-c', dest='isClean', default=False, type=bool, help='work option: clean or process')

	args = parser.parse_args()

	if args.isClean is None:
		parser.print_help()
		return None
	return args

if __name__ == '__main__':
	args = getargs()
	if args is None:
		exit(1)

	if args.isClean is True:
		clear(args.group, args.project)
	else:
		work(args.group, args.project)
