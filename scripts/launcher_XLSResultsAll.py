#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

from commons import Subjects
from results import XLSResultAll

def getargs():
	import argparse
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('-w', dest='workType', default=None, help='workType : Experiment Result Name')

	args = parser.parse_args()

	if args.workType is None:
		parser.print_help()
		return None
	return args

if __name__ == '__main__':
	args = getargs()
	if args is None:
		exit(1)

	S = Subjects()
	name = args.workType
	result_xls = os.path.join(S.root_result, ('Result_%s.xlsx' % name))

	obj = XLSResultAll(result_xls)
	obj.run(S, name, _isUnion=False)
