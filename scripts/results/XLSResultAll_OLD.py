#-*- coding: utf-8 -*-
'''
Created on 2016. 11. 19
Updated on 2016. 01. 09
'''

import os

from commons import Previous
from commons import VersionUtil
from results import Evaluator
from results import XLSbasic
from utils import Progress


class XLSResultAllOLD(XLSbasic):
	__name__ = 'ResultXLSAll_OLD'

	#######################################################################
	# Data Summary Part Process
	#######################################################################
	def create_SummarySheet(self, _startCol):
		sheet = self.workbook.add_worksheet('Summary')
		texts = ['Technique', 'Group', 'Project', 'SourceCount', 'BugCount', 'Recommended BugCount', 'Top1 Count', 'Top5 Count', 'Top10 Count', 'Top1', 'Top5', 'Top10', 'MAP', 'MRR']
		self.set_cols(sheet, col=_startCol, widths=[17, 17, 17, 14, 10, 14, 7, 7, 7, 7, 7, 7, 7, 7])
		self.input_row(sheet, row=0, col=_startCol, values=texts, default_style=self.title_format)

		sheet.freeze_panes(1, 0)  # Freeze the second row.
		self.summary_row = 1
		return sheet

	def fill_SummarySheet(self, _sheet, _group, _program, _project, _item, _srcCnt, _bugCnt, _bugCntR):
		styles = [self.subtitle_format] * 3 + [self.number_format] * 6 + [self.percent_format] * 5
		values = [_program, _group, _project, _srcCnt, _bugCnt, _bugCntR,
		          _item.top1, _item.top5, _item.top10,
		          _item.top1P, _item.top5P, _item.top10P,
		          _item.MAP, _item.MRR]
		self.input_row(_sheet, self.summary_row, 0, values, styles)
		self.summary_row += 1
		return self.summary_row

	#######################################################################
	# Raw Data Part Process
	#######################################################################
	def create_DataSheet(self, _startCol):
		sheet = self.workbook.add_worksheet('rawData')

		self.set_cols(sheet, 0, widths=[5, 12, 12, 12, 8, 12, 12, 25, 6, 12, 7, 7, 7, 10, 8, 8, 8])

		texts = ['key', 'Approach', 'Group', 'Project', 'BugID',
		         'Version', 'AnsFileCount', 'File', 'Rank', 'Score',
		         'Top1', 'Top5', 'Top10',
		         'AnsOrder', 'P(rank)', 'AP', 'TP']
		self.input_row(sheet, row=0, col=_startCol, values=texts, default_style=self.title_format)

		sheet.freeze_panes(1, 0)  # Freeze the second row.
		self.data_row = 1
		return sheet

	def fill_DataSheet(self, _sheet, _program, _group, _project, _bugData, _rawData, _ansCounts):
		#Write data and make basic statistics
		styles = [self.id_format]*6 + [self.number_format, self.base_format, self.number_format, self.float_format]+ \
		         [self.number_format]*4 + [self.float_format]*3

		data_keys = _rawData.keys()
		data_keys.sort()
		maxScore = 0.0
		for bugID in data_keys:
			for this in _rawData[bugID]:
				if maxScore < this.score: maxScore = this.score

		for bugID in data_keys:
			AP = _bugData[bugID].AP
			count = _ansCounts[bugID]

			for this in _rawData[bugID]:			# for each bug id's results
				key = '%s%d'%(_project.lower(),this.id)
				values = [key,
				          _program, _group, _project, this.id, 'all', count, this.filename, this.rank, this.score,
				          this.top1, this.top5, this.top10, this.AnsOrder, this.AP, AP, this.TP]

				self.input_row(_sheet, self.data_row, 0, values, styles)
				self.data_row += 1
		return self.data_row

	#######################################################################
	# Raw Data Part Process
	#######################################################################
	def create_bugDataSheet(self, _startCol):
		sheet = self.workbook.add_worksheet('bugData')

		self.set_cols(sheet, 0, widths=[5, 12, 12, 12, 8, 12, 12, 6, 6, 6, 7, 7, 8, 8, 8])

		texts = ['key', 'Approach', 'Group', 'Project', 'BugID', 'Version', 'AnsFileCount', 'Top1', 'Top5', 'Top10', 'AP', 'TP',
		         'Pin(1)', 'Pin(5)', 'Pin(10)']
		self.input_row(sheet, row=0, col=_startCol, values=texts, default_style=self.title_format)

		sheet.freeze_panes(1, 0)  # Freeze the second row.
		self.bug_row = 1
		return sheet

	def fill_bugDataSheet(self, _sheet, _program, _group, _project,_bugData, _ansCounts):
		#Write data and make basic statistics
		data_keys = _bugData.keys()
		data_keys.sort()
		styles = [self.id_format]*6 + [self.number_format]*4 + [self.float_format]*5

		for bugID in data_keys:
			this = _bugData[bugID]			# for each bug id's results
			count = _ansCounts[this.id]
			key = '%s%d'%(_project.lower(),this.id)
			values = [key, _program, _group, _project, this.id, 'all', count, this.top1, this.top5, this.top10, this.AP, this.TP]

			values.append(this.top1 / float(count if count <= 1 else 1))
			values.append(this.top5 / float(count if count <= 5 else 5))
			values.append(this.top10 / float(count if count <= 10 else 10))

			self.input_row(_sheet, self.bug_row, 0, values, styles)

			self.bug_row += 1
		return self.bug_row


	#######################################################################
	# Data Subject Part Process
	#######################################################################
	def create_SubjectSheet(self, _startCol):
		sheet = self.workbook.add_worksheet('Subjects')

		self.set_cols(sheet, col=0, widths=[15, 17, 15, 15, 15, 5, 15, 17, 20, 15, 15])
		self.input_colspan(sheet, row=0, col=0, span=5, values=['Summary'], default_style=self.title_format)
		self.input_colspan(sheet, row=0, col=6, span=5, values=['Details'], default_style=self.title_format)

		self.set_rows(sheet, row=1, heights=[50])
		texts = ['Group', 'Project', 'Bug Reports\n(Sum)', 'Duplicate\nBug Reports\n(Sum)', 'Source Files\n(Max)']
		self.input_row(sheet, row=1, col=0, values=texts, default_style=self.title_format)

		texts = ['Group', 'Project', 'Version', 'Bug Reports', 'Source Files']
		self.input_row(sheet, row=1, col=6, values=texts, default_style=self.title_format)

		formulas = ['=sum(D4:D5000)', '=sum(E4:E5000)', '=sum(F4:F5000)']
		self.input_row(sheet, row=2, col=2, values=formulas, default_style=self.subtitle_number_format)

		formulas = ['=sum(K4:K50000)', '=sum(L4:L50000)']
		self.input_row(sheet, row=2, col=9, values=formulas, default_style=self.subtitle_number_format)

		sheet.freeze_panes(3, 0)  # Freeze the second row.
		self.subj_summary_row = 3
		self.subj_data_row = 3
		return sheet

	def fill_SubjectSheet(self, _sheet, _group, _srcCounts, _bugCounts, _dupCounts):
		projects = _bugCounts.keys()
		projects.sort()

		size = sum([len(_bugCounts[project]) for project in projects])
		progress = Progress('[%s] fill subject' % self.__name__, 2, 10, True)
		progress.set_point(0).set_upperbound(size)
		progress.start()

		styles = [self.base_format, self.base_format, self.base_format, self.number_format, self.number_format]
		for project in projects:
			for version in _bugCounts[project].keys():
				if version == 'all': continue
				values = [_group, project, version.upper(), _bugCounts[project][version], _srcCounts[project][version]]
				self.input_row(_sheet, self.subj_data_row, 6, values, styles)
				self.subj_data_row += 1
				progress.check()
		progress.done()

		#summary
		styles = [self.subtitle_format, self.subtitle_format, self.number_format, self.number_format, self.number_format]
		for project in projects:
			values = [_group, project.upper(),  _bugCounts[project]['all'], _dupCounts[project], _srcCounts[project]['all']]
			self.input_row(_sheet, self.subj_summary_row, 0, values, styles)
			self.subj_summary_row += 1
		pass

	#######################################################################
	# Data Subject Part Process
	#######################################################################
	def create_DescriptionSheet(self):
		'''
		:return:
		'''
		titles = ['Sheet', 'Columns', 'Description', 'Reference']
		texts = [
			['Summary', 'Approach', 'The technique that one of AmaLgam, BLIA, BLUiR, BugLocator, BRTracer, Locus', ''],
			['Summary', 'Group', 'Project group name (Apache, Apache Commons, Jboss, Wildfly, Spring)', ''],
			['Summary', 'Project', 'Project Name', ''],
			['Summary', 'BugCount', 'The number of bug count', ''],
			['Summary', 'Top1 Count', 'The count of bugs that Top1 is true', ''],
			['Summary', 'Top5 Count', 'The count of bugs that Top5 is true', ''],
			['Summary', 'Top10 Count', 'The count of bugs that Top10 is true', ''],
			['Summary', 'Top1', 'Top1 Count / # of Bugs', ''],
			['Summary', 'Top5', 'Top5 Count / # of Bugs', ''],
			['Summary', 'Top10', 'Top10 Count / # of Bugs', ''],
			['Summary', 'MAP', '', 'https://en.wikipedia.org/wiki/Information_retrieval#Mean_average_precision'],
			['Summary', 'MRR', '', ''],
			['rawData', 'Approach', 'The technique that one of AmaLgam, BLIA, BLUiR, BugLocator, BRTracer, Locus', ''],
			['rawData', 'Group', 'Project group name (Apache, Apache Commons, Jboss, Wildfly, Spring)', ''],
			['rawData', 'Project', 'Project Name (Subject)', ''],
			['rawData', 'BugID', 'The ID of bug report', ''],
			['rawData', 'Version', 'The source code version related a bug report', ''],
			['rawData', 'AnsFileCount', 'The number of fixed files (this is for bug level value)', ''],
			['rawData', 'File', 'the fixed file name', ''],
			['rawData', 'Rank', 'the ranking of a fixed file (The rank starts from 0)', ''],
			['rawData', 'Score', 'The suspicious score from specific technique [0, 1]', ''],
			['rawData', 'normalRank', '( Rank + 1) / the number of SourceCode Files ', ''],
			['rawData', 'normalScore', 'score / maximum value of score in specific technique', ''],
			['rawData', 'Top1', '1 if the answer file is ranked in top 1 (0=False, 1=True)', ''],
			['rawData', 'Top5', '1 if the answer file is ranked in top 5 (0=False, 1=True)', ''],
			['rawData', 'Top10', '1 if the answer file is ranked in top 10 (0=False, 1=True)', ''],
			['rawData', 'AnsOrder', 'The ranking value of each answer file in a bug report (the rank start 0)', ''],
			['rawData', 'P(rank)',  'the precision of a answer file (this used for calculating MAP',
			 'https://en.wikipedia.org/wiki/Information_retrieval#Mean_average_precision'],
			['rawData', 'TP', 'Top Precision, the precision of file that is ranked on top (other ranking files are 0)', 'https://en.wikipedia.org/wiki/Mean_reciprocal_rank'],
			['rawData', 'DupType', 'Master:core bug report in duplicated set / Duplicate: duplicated bug report in duplicated set / None: this is not related with duplication)', ''],
			['rawData', 'DupID', 'duplicate bug report ID', ''],
			['rawData', 'Talks', 'Attribute of bug report : True if talks is exists in a bug report (extracted from Infozilla)', ''],
			['rawData', 'Enums', 'Attribute of bug report : True if talks is enumeration in a bug report (extracted from Infozilla)', ''],
			['rawData', 'Code', 'Attribute of bug report: True if talks is code region in a bug report (extracted from Infozilla)', ''],
			['rawData', 'Stack', 'Attribute of bug report : True if talks is stack trace in a bug report (extracted from Infozilla)', ''],
			['rawData', 'CountSummaryHints',
			 'Attribute of bug report : the number of Hint keywords in summary in bug report (class, package, method name, and so on.)', ''],
			['rawData', 'CountDescHints',
			 'Attribute of bug report : the number of Hint keywords in description in bug report (class, package, method name, and so on.)', ''],
			['bugData', '-', 'Sheet Description : The summary information of each bug report', ''],
			['bugData', 'AP', 'The average of precision for the all answers in a bug report', ''],
			['bugData', 'TP', 'Top Precision, the precision of file that is ranked on top (this used for MRR)', '']
		]

		sheet = self.workbook.add_worksheet('Description')
		self.set_cols(sheet, col=0, widths=[8, 25, 100, 30])
		self.input_row(sheet, row=0, col=0, values=titles, default_style=self.title_format)
		row = 1
		styles = [self.id_format, self.id_format, self.base_format, self.base_format]
		for text in texts:
			self.input_row(sheet, row=row, col=0, values=text, styles=styles, default_style=self.base_format)
			row +=1

		sheet.freeze_panes(1, 0)  # Freeze the second row.
		pass

	#######################################################################
	# Overall Process
	#######################################################################

	def get_countings(self, _group, _project, _tech):
		from Counting import Counting
		counter = Counting()
		if _tech == 'BLIA' and _project in ['AspectJ', 'SWT', 'ZXing']:
			filename = 'BLIA_repository.xml'
		elif _tech == 'Locus' and _project == 'AspectJ':
			filename = 'Locus_repository.xml'
		else:
			filename = 'repository.xml'
		repoPath = os.path.join(self.S.getPath_bugrepo(_group, _project), filename)
		answers = counter.getAnswers(repoPath)
		bugs = counter.getBugs(repoPath)

		# make the count of source code
		cache = os.path.join(self.S.getPath_base(_group, _project), 'sources.txt')
		if os.path.exists(cache) is False:
			print('making sourcecode counts...', end='')
			counts = {_project:{}}
			baseCodePath = self.S.getPath_source(_group, _project)
			for dir in os.listdir(baseCodePath):
				counts[_project][dir] = counter.getCodeCount(os.path.join(baseCodePath,dir))
			from utils.PrettyStringBuilder import PrettyStringBuilder
			builder = PrettyStringBuilder(_indent_depth=2)
			text = builder.get_dicttext(counts)
			f = open(cache, 'w')
			f.write(text)
			f.close()
			print('Done.')

		#read the count of source code
		f = open(cache, 'r')
		text = f.read()
		f.close()
		data = eval(text)
		vname = VersionUtil.get_versionName(self.S.get_max_versions(_tech, _project), _project)
		sources = data[_project][vname]

		return sources, bugs, answers

	def append_project(self, _group, _project, _tech):

		sources, bugs, answers = self.get_countings(_group, _project, _tech)
		resultFiles = []
		resultFiles.append(self.S.getPath_results(self.TYPE, _tech, _group, _project, 'all'))

		ev = Evaluator(_tech, _project)
		ev.load(resultFiles)
		ev.evaluate(answers, len(bugs))

		self.fill_SummarySheet(self.summarySheet, _group, _tech, _project, ev.projectSummary, sources, len(bugs), len(ev.bugSummaries))
		self.fill_bugDataSheet(self.bugSheet, _tech, _group, _project, ev.bugSummaries, answers)
		self.fill_DataSheet(self.dataSheet, _tech, _group, _project, ev.bugSummaries, ev.rawData, answers)
		pass

	def run(self, _type):
		'''
		create result file
		'''
		self.TYPE = _type

		# XLS preparing
		self.summarySheet = self.create_SummarySheet(0)
		self.dataSheet = self.create_DataSheet(0)
		self.bugSheet = self.create_bugDataSheet(0)

		self.S = Previous()
		for group in self.S.groups:
			for project in self.S.projects[group]:
				print('working %s / %s ...' % (group, project))
				for tech in self.S.techniques:
					self.append_project(group, project, tech)
		self.finalize()
		pass

###############################################################################################################
###############################################################################################################
###############################################################################################################
if __name__ == "__main__":
	name = 'PreviousData'
	obj = XLSResultAllOLD('/mnt/exp/Bench4BL/expresults/Result_%s.xlsx' % name)
	obj.run(name)
	pass
