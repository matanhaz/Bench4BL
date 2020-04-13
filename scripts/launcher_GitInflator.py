#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os, stat
import shutil

from commons import Subjects
from repository import GitInflator

# Make works

def del_rw(action, name, exc):
	os.chmod(name, stat.S_IWRITE)
	os.remove(name)

def make(_sGroup=None, _sProject=None):
	S = Subjects()
	for group in S.groups:
		if _sGroup is None or group == _sGroup:
			for project in S.projects[group]:
				if _sProject is None or project == _sProject:
					git = GitInflator(project, S.getPath_base(group, project))
					git.inflate(S.versions[project])  # The items in versions is git tag name map with each version.

def clear(_sGroup=None, _sProject=None):
	S = Subjects()
	for group in S.groups:
		if _sGroup is None or group == _sGroup:
			for project in S.projects[group]:
				if _sProject is None or project == _sProject:
					target = S.getPath_source(group, project)
					try:
						shutil.rmtree(target, onerror=del_rw)
						print(u'removed: %s' % target)
					except Exception as e:
						print(u'failed to remove : %s' %target)

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
		make(args.group, args.project)
