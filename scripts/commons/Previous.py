#-*- coding: utf-8 -*-
'''
Created on 2017. 02. 16
Updated on 2017. 02. 16
'''

import os
from commons import Subjects


class Previous(Subjects):
	'''
	Collecting Subjects information
	Sourcecode, Bug reports, Duplicate bug reports
	'''
	__name__ = 'Previous'
	groups = ['Previous']
	projects = {
		'Previous': ['AspectJ', 'ZXing', 'PDE', 'JDT', 'SWT']
	}

	def __init__(self):
		super(Previous, self).__init__()
		pass

	def get_max_versions(self, _technique, _project):
		versions = {
			'AspectJ': '1.6.0.M2',  # BLIA = 1.5.3.final
			'JDT': '4.5',
			'PDE': '4.4',
			'SWT': '3.138',  # BLIA = 3.659
			'ZXing': '1.6',
		}
		if _technique == "BLIA":
			if _project == "AspectJ": return '1.5.3.final'
			if _project == "SWT": return '3.659'
		#if _technique == "Locus":
		#if _project == "SWT": return u'3.138.GIT'

		return versions[_project]