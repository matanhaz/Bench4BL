#!/usr/bin/env python
#-*- coding: utf-8 -*-


import os
import shutil

from commons import Subjects
from repository import DupMergeRepositoryMaker

def clean():
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

def work():
	obj = DupMergeRepositoryMaker()
	S = Subjects()
	for group in S.groups:
		for project in S.projects[group]:
			obj.make(group, project)

work()
