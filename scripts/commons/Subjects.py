#*- coding: utf-8 -*-

'''
Created on 2017. 02. 16
Updated on 2017. 02. 16
'''

import os

here = os.path.dirname(os.path.abspath(__file__))

class Subjects(object):
	'''
	Collecting Subjects information
	Sourcecode, Bug reports, Duplicate bug reports
	'''
	__name__ = 'Subjects'
	root = os.path.join(here, '../../data/')
	root_result = os.path.join(here, '../../expresults/')
	techniques = ['BugLocator', 'BRTracer', 'BLUiR', 'AmaLgam', 'BLIA', 'Locus']
	groups = ['Apache', 'Commons', 'JBoss', 'Wildfly', 'Spring']
	projects = {
		'Apache':['CAMEL', 'HBASE', 'HIVE'],
		'Commons':['CODEC', 'COLLECTIONS', 'COMPRESS', 'CONFIGURATION', 'CRYPTO', 'IO', 'LANG', 'MATH', 'WEAVER','CSV'],
		'JBoss':['ENTESB', 'JBMETA'],
		'Wildfly':['ELY', 'WFARQ', 'WFCORE', 'WFLY', 'WFMP','SWARM'],
		'Spring':['AMQP', 'ANDROID', 'BATCH', 'BATCHADM', 'DATACMNS', 'DATAGRAPH', 'DATAJPA', 'DATAMONGO', 'DATAREDIS', 'DATAREST', 'LDAP', 'MOBILE', 'ROO', 'SEC', 'SECOAUTH', 'SGF', 'SHDP', 'SHL', 'SOCIAL', 'SOCIALFB', 'SOCIALLI', 'SOCIALTW', 'SPR', 'SWF', 'SWS']
	}

	urls = {
		'HBASE': 'https://github.com/apache/hbase.git',
		'HIVE': 'https://github.com/apache/hive.git',
		'CAMEL': 'https://github.com/apache/camel.git',

		'MATH': 'https://github.com/apache/commons-math.git',
		'LANG': 'https://github.com/apache/commons-lang.git',
		'IO': 'https://github.com/apache/commons-io.git',
		'COLLECTIONS': 'https://github.com/apache/commons-collections.git',
		'CODEC': 'https://github.com/apache/commons-codec.git',
		'WEAVER': 'https://github.com/apache/commons-weaver.git',
		'CONFIGURATION': 'https://github.com/apache/commons-configuration.git',
		'CSV': 'https://github.com/apache/commons-csv.git',
		'COMPRESS': 'https://github.com/apache/commons-compress.git',
		'CRYPTO': 'https://github.com/apache/commons-crypto.git',

		'ENTESB': 'https://github.com/jboss-fuse/fuse.git',
		'JBMETA': 'https://github.com/jboss/metadata.git',

		'ELY': 'https://github.com/wildfly-security/wildfly-elytron.git',
		'SWARM': 'https://github.com/wildfly-swarm/wildfly-swarm.git',
		'WFARQ': 'https://github.com/wildfly/wildfly-arquillian.git',
		'WFCORE': 'https://github.com/wildfly/wildfly-core.git',
		'WFLY': 'https://github.com/wildfly/wildfly.git',
		'WFMP': 'https://github.com/wildfly/wildfly-maven-plugin.git',

		'ANDROID': 'https://github.com/spring-projects/spring-android',
		'AMQP': 'https://github.com/spring-projects/spring-amqp',
		'BATCH': 'https://github.com/spring-projects/spring-batch',
		'BATCHADM': 'https://github.com/spring-projects/spring-batch-admin',
		'DATACMNS': 'https://github.com/spring-projects/spring-data-commons',
		'DATAJPA': 'https://github.com/spring-projects/spring-data-jpa',
		'DATAMONGO': 'https://github.com/spring-projects/spring-data-mongodb',
		'DATAGRAPH': 'https://github.com/spring-projects/spring-data-neo4j',
		'DATAREDIS': 'https://github.com/spring-projects/spring-data-redis',
		'DATAREST': 'https://github.com/spring-projects/spring-data-rest',
		'LDAP': 'https://github.com/spring-projects/spring-ldap',
		'MOBILE': 'https://github.com/spring-projects/spring-mobile',
		'ROO': 'https://github.com/spring-projects/spring-roo',
		'SECOAUTH': 'https://github.com/spring-projects/spring-security-oauth',
		'SHL': 'https://github.com/spring-projects/spring-shell',
		'SOCIAL': 'https://github.com/spring-projects/spring-social',
		'SOCIALFB': 'https://github.com/spring-projects/spring-social-facebook',
		'SOCIALLI': 'https://github.com/spring-projects/spring-social-linkedin',
		'SOCIALTW': 'https://github.com/spring-projects/spring-social-twitter',
		'SPR': 'https://github.com/spring-projects/spring-framework',
		'SWF': 'https://github.com/spring-projects/spring-webflow',
		'SWS': 'https://github.com/spring-projects/spring-ws',
		'SGF': 'https://github.com/spring-projects/spring-data-gemfire',
		'SHDP': 'https://github.com/spring-projects/spring-hadoop',
		'SEC': 'https://github.com/spring-projects/spring-security',
		# 'SOCIALGH':'https://github.com/spring-projects/spring-social-github',
	}

	###
	# versions has all available source code version
	versions = {}

	# the distribution of bug reports' ID in each version
	# if there are no bug reports in a version, the bugs not include the key according to version.
	bugs = {}
	answers = {}
	sources = {}
	duplicates = {}
	duplicate_sets = {}
	answers_merge = {}

	def __init__(self):
		# make version informations
		self.versions = {}
		self.bugs = {}
		for group in self.groups:
			for project in self.projects[group]:
				if not os.path.exists(self.getPath_base(group, project)):
					continue
				self.versions[project] = self.load_versions(group, project)
				self.bugs[project] = self.load_bugs(group, project)
				self.sources[project] = self.load_sources(group, project)
				self.answers[project] = self.load_answers(group, project)
				self.duplicates[project] = self.load_duplicates(group, project)
				self.duplicate_sets[project] = set([])
				for dup in self.duplicates[project]:
					self.duplicate_sets[project].update(dup)
				self.answers_merge[project] = self.load_answers(group, project, 'answers_merge.txt')

				# sumBugs = 0
				# for version in self.bugs[project]:
				# 	if version == 'all': continue
				# 	sumBugs += len(self.bugs[project][version])
				# print('%s\t%s\t%d\t%d' % (group, project, len(self.bugs[project]['all']), sumBugs))
		self.complement_duplicates()
		pass

	def complement_duplicates(self):
		if len(self.duplicates) <= 0: return False

		def make(_duplicates):
			flagWorked = False
			newDups = list()
			for srcA, destA in _duplicates:
				newSrc = None
				for srcB, destB in _duplicates:
					if srcA == destB:
						newSrc = srcB
						break
				if newSrc is None:
					newDups.append([srcA, destA])
				else:
					newDups.append([newSrc, destA])
					flagWorked = True
			return newDups, flagWorked

		for project in self.duplicates:
			while True:
				newDups, flag = make(self.duplicates[project])
				if flag is False: break
				self.duplicates[project] = newDups
		return True

	def load_sources(self, _group, _project):
		filename =os.path.join(self.getPath_base(_group, _project), 'sources.txt')
		if os.path.exists(filename) is False:
			return {}
		f = open(filename, 'r')
		text = f.read()
		f.close()
		data = eval(text)
		if 'miss' in data[_project]: del data[_project]['miss']

		return data[_project]

	def load_answers(self, _group, _project, _name=None):
		if _name is not None:
			filename = os.path.join(self.getPath_base(_group, _project), _name)
		else:
			filename = os.path.join(self.getPath_base(_group, _project), 'answers.txt')

		if os.path.exists(filename) is False:
			return {}
		f = open(filename, 'r')
		text = f.read()
		f.close()
		data = eval(text)
		if 'miss' in data[_project]: del data[_project]['miss']

		return data[_project]

	def load_bugs(self, _group, _project):
		filename =os.path.join(self.getPath_base(_group, _project), 'bugs.txt')
		if os.path.exists(filename) is False:
			return {}
		f = open(filename, 'r')
		text = f.read()
		f.close()
		data = eval(text)
		if 'miss' in data[_project]: del data[_project]['miss']

		return data[_project]

	def load_duplicates(self, _group, _project):
		filename = os.path.join(self.getPath_bugrepo(_group, _project), 'duplicates.json')
		if os.path.exists(filename) is False:
			return {}
		f = open(filename, 'r')
		text = f.read()
		f.close()
		data = eval(text)
		nd = {}
		for key in data:
			nd[key.upper()] = data[key]
		return nd[_project.upper()]

#	def load_versions(self, _group, _project):
#		f = open(os.path.join(self.getPath_base(_group, _project), 'versions.txt'), 'r')
#		text = f.read()
#		f.close()
#		data = eval(text)
#
#		return data[_project]
	
	def load_versions(self, _group, _project):
		f = open(os.path.join(self.getPath_base(_group, _project), 'versions.txt'), 'r')
		text = f.read()
		f.close()
		data = eval(text)
		
		ret = data[_project]
		
		ret["1.11"] ="1.11"
		ret["1.12"] ="1.12"
		ret["1.13"] ="1.13"
		ret["1.14"] ="1.14"
		ret["1.15"] ="1.15"
		ret["1.16"] ="1.16"
	
# 		ret["1.1"] ="CODEC_1_1"
# 		ret["1.2"] ="CODEC_1_2"

		return ret

	####################################################
	# path functions
	####################################################
	def getPath_bugrepo(self, _group, _project):
		return os.path.join(self.root, _group, _project, 'bugrepo')

	def getPath_source(self, _group, _project, _version=None):
		if _version is None:
			return os.path.join(self.root, _group, _project, 'sources')
		return os.path.join(self.root, _group, _project, 'sources', _version)

	def getPath_gitrepo(self, _group, _project):
		return os.path.join(self.root, _group, _project, 'gitrepo')

	def getPath_base(self, _group, _project):
		return os.path.join(self.root, _group, _project)

	def getPath_results(self, _type, _tech, _group, _project, _version):
		return os.path.join(self.root_result, _type, _group, _project, '%s_%s_%s_output.txt'%(_tech, _project, _version))

	def getPath_result_folder(self, _type, _group, _project):
		return os.path.join(self.root_result, _type, _group, _project)

