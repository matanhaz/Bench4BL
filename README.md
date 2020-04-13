# Bench4BL

Bench4BL is a collection of bug reports and corresponding source code files to fix a bug specified by each bug report to support bug localization research. This collection contains 10,017 bug reports collected from 51 open source projects, and each bug report is mapped with the source code files of the corresponding version. Therefore, this dataset can help researchers and practitioners evaluate bug localization techniques with a large number of subjects.

## File Structure

Traced:

- `bootstrap`: Scripts for download and unarchive bug repositories
- `scripts`: Launch scripts in Python 2
    - `repository`: Scripts to prepare the resources to execute each technique
    - `results`: Scripts to collect the execution results of each technique and export to Excel
    - `analysis`: Scripts to analysis for the result of each technique and features extracted from resources. We applied Mann-Whitney U test, Pearson correlation and so on
    - `commons`: Scripts to managing subjects and common functions
    - `utils`: Personal libraries for experiments
- `src`: Techniques source code
- `techniques`: Techniques executables
    - `packing.sh`: Shell script to pack resources for each subject
    - `unpacking.sh`: Shell script to unpack resources for each subject

Generated:

- `venv`: Python 2 virtual environment
- `archives`: Downloaded bug repositories
- `data`: Unarchived bug repositories
- `depots`: Executables
- `expresults`: Experiment results

## Build

### Prerequisites

Install the latest version of Arch Linux.

```sh
# pacman -S base-devel jre-openjdk-headless python2 python-virtualenv
```

### Download Bug Repositories

```sh
$ cd `git rev-parse --show-toplevel`
$ bootstrap/downloads.sh
```

### Configuration

In `scripts/commons/Subjects.py`, there are variables that stores a resource PATH information as a string and subject information. To use our scripts, you should change the variables properly. You should use absolute PATH to update the PATH information and use the same subject name with subject Directory name for the subject information.

- `techniques`: The list of previous technique names.
- `groups`: The list of group names that you want to test.
- `projects`: The list of subject names that you want to test. Each subject name should be classified into specific group name.

You should also modify `scripts/launcher_Tool.py`.

### Unarchive

```sh
$ mkdir data
$ bootstrap/unpacking.sh ./archives ./data Apache HIVE
```

### Install Indri

To execute BLUiR and AmaLgam, you need to install indri. indri-5.15 can work.

```sh
$ mkdir depots
$ cd depots
$ wget https://excellmedia.dl.sourceforge.net/project/lemur/lemur/indri-5.15/indri-5.15.tar.gz
$ tar -xzf indri-5.15.tar.gz
$ cd indri-5.15
$ ./configure --prefix=`pwd`/../install
$ make
$ make install
```

Edit `Settings.txt` file:

```sh
$ echo indripath=`git rev-parse --show-toplevel`/depots/install/bin/ > `git rev-parse --show-toplevel`/techniques/Settings.txt
```

### Create Virtual Environment

```sh
$ cd `git rev-parse --show-toplevel`
$ virtualenv venv -p `which python2`
$ pip install -r requirements.txt
```

### Build JAR

```sh
$ bootstrap/buildjar.sh
```

## Run

### Source Virtual Environment

```sh
$ cd `git rev-parse --show-toplevel`
$ . venv/bin/activate
```

### Modify PATH

```sh
$ export PATH=$PATH:`pwd`/depots/install/bin
```

### Inflate the source codes

We used multiple versions of source code for the experiment. Since the provided archives have only a git repository, you need to check out repositories according to versions that you selected above. The script `launcher_GitInflator.py` clones a git repositories and checks it out into the multiple versions which you selected. These source codes are stored into a folder `Bench4BL/data/[Group Name]/[Project Name]/sources/` automatically.

```sh
$ cd `git rev-parse --show-toplevel`/scripts
$ python launcher_GitInflator.py
```

### Build bug repositories

We need to build a repository for the bug reports with pre-crawled bug reports. The bug repository is in XML format and includes bug data which is used in the experiments. The `launcher_repoMaker.py` makes the bug repository that containing entire crawled bug reports information and bug repositories that stores bug reports according to the mapped version. But, since we already offer the result of this step in provided subject's archives, use this script if you want to update the bug repositories. The `launcher_DupRepo.py` creates a bug repository file that contains bug information merged duplicate bug reports.

```sh
$ python launcher_repoMaker.py
$ python launcher_DupRepo.py
```

### Update count information of bug and source codes

The script of Counting.py makes a count information for bug and source code. The result will be stored `bugs.txt`, `sources.txt` and `answers.txt` in each subject's folder.

```sh
$ python Counting.py
```

### Execute Previous Techniques

To get the result of each technique, you can use `scripts/launcher_Tool.py`. The script executes 6 techniques for all subjects.

The script basically works for the multiple versions of bug repository and each of the related source codes. We explain what you need to run the tool first and describe the tool usage.

```sh
$ mkdir -p ../techniques/locus_properties
$ python launcher_Tool.py -w Exp1
```

Usage of `launcher_Tool.py`:

**Prerequisites**

- You need to set the PATHs and JavaOptions in the `launcher_Tool.py` file.
- Open the file, launcher_Tool.py and check the following variables 
- ProgramPATH: Set the directory path which contains the release files of the IRBL techniques. (ex. u'~/Bench4BL/techniques/')
- OutputPATH: Set the result path to save output of each technique (ex. u'~/Bench4BL/expresults/')
- JavaOptions: Set the java command options. (ex. `-Xms512m -Xmx4000m`)
- JavaOptions_Locus: Set the java options for Locus. Because Locus need a large memory, we separated the option. (ex. `-Xms512m -Xmx8000m`)

**Options**

- -w <work name>: \[necessary\] With this option, users can set the ID for each experiment, and each ID is also used as a directory name to store the execution results of each Technique. Additionally, if the name starts with "Old", this script works for the previous data, otherwise works for the new data.
- -g <group name>: A specific group. With this option, the script works for the subjects in the specified group. 
- -p <subject name>: A specific subject. To use this option, you should specify the group name. 
- -t <technique name>: A specific technique. With this option, the script makes results of specified technique.
- -v <version name>: A specific version. With this option, the script works for the specified version of source code.
- -s: Single version mode, With this option, the script works for the only latest source code.
- -m: With this option, the bug repositories created by combining the text of duplicate bug report pairs are used instead of the normal one.

**Examples**

```sh
$ python launcher_Tool.py -w ExpFirst
$ python launcher_Tool.py -w ExpFirst -s
$ python launcher_Tool.py -w ExpFirst_Locus -t Locus
$ python launcher_Tool.py -w ExpFirst_CAMLE -g Apache -p CAMEL
```

## Subjects (Bug reports and Source Code Repositories)

The following table shows five old subjects that used in previous studies and 46 new subjects that we newly collected.

The subjects are classified into six groups (the five subjects used in previous studies are grouped as "Old subjects").

Each subject consists of bug reports, bug report repositories that we refined, cloned git repository, and metadata of them that we curated. If you need a recent git repository, please clone the repository again by using a link in the "Git Repository" column.

| Group | Subject | Archive | Git Repository |
| :- | :- | :- | :- |
| Apache | CAMEL | [CAMEL.tar](https://sourceforge.net/projects/irblsensitivity/files/Apache/CAMEL.tar) | [apache/camel](https://github.com/apache/camel) |
| Apache | HBASE | [HBASE.tar](https://sourceforge.net/projects/irblsensitivity/files/Apache/HBASE.tar) | [apache/hbase](https://github.com/apache/hbase) |
| Apache | HIVE | [HIVE.tar](https://sourceforge.net/projects/irblsensitivity/files/Apache/HIVE.tar) | [apache/hive](https://github.com/apache/hive) |
| Commons | CODEC | [CODEC.tar](https://sourceforge.net/projects/irblsensitivity/files/Commons/CODEC.tar) | [apache/commons-codec](https://github.com/apache/commons-codec) |
| Commons | COLLECTIONS | [COLLECTIONS.tar](https://sourceforge.net/projects/irblsensitivity/files/Commons/COLLECTIONS.tar) | [apache/commons-collections](https://github.com/apache/commons-collections) |
| Commons | COMPRESS | [COMPRESS.tar](https://sourceforge.net/projects/irblsensitivity/files/Commons/COMPRESS.tar) | [apache/commons-compress](https://github.com/apache/commons-compress) |
| Commons | CONFIGURATION | [CONFIGURATION.tar](https://sourceforge.net/projects/irblsensitivity/files/Commons/CONFIGURATION.tar) | [apache/commons-configuration](https://github.com/apache/commons-configuration) |
| Commons | CRYPTO | [CRYPTO.tar](https://sourceforge.net/projects/irblsensitivity/files/Commons/CRYPTO.tar) | [apache/commons-crypto](https://github.com/apache/commons-crypto) |
| Commons | CSV | [CSV.tar](https://sourceforge.net/projects/irblsensitivity/files/Commons/CSV.tar) | [apache/commons-csv](https://github.com/apache/commons-csv) |
| Commons | IO | [IO.tar](https://sourceforge.net/projects/irblsensitivity/files/Commons/IO.tar) | [apache/commons-io](https://github.com/apache/commons-io) |
| Commons | LANG | [LANG.tar](https://sourceforge.net/projects/irblsensitivity/files/Commons/LANG.tar) | [apache/commons-lang](https://github.com/apache/commons-lang) |
| Commons | MATH | [MATH.tar](https://sourceforge.net/projects/irblsensitivity/files/Commons/MATH.tar) | [apache/commons-math](https://github.com/apache/commons-math) |
| Commons | WEAVER | [WEAVER.tar](https://sourceforge.net/projects/irblsensitivity/files/Commons/WEAVER.tar) | [apache/commons-weaver](https://github.com/apache/commons-weaver) |
| JBoss | ENTESB | [ENTESB.tar](https://sourceforge.net/projects/irblsensitivity/files/JBoss/ENTESB.tar) | [jboss-fuse/fuse](https://github.com/jboss-fuse/fuse) |
| JBoss | JBMETA | [JBMETA.tar](https://sourceforge.net/projects/irblsensitivity/files/JBoss/JBMETA.tar) | [jboss/metadata](https://github.com/jboss/metadata) |
| Wildfly | ELY | [ELY.tar](https://sourceforge.net/projects/irblsensitivity/files/Wildfly/ELY.tar) | [wildfly-security/wildfly-elytron](https://github.com/wildfly-security/wildfly-elytron) |
| Wildfly | SWARM | [SWARM.tar](https://sourceforge.net/projects/irblsensitivity/files/Wildfly/SWARM.tar) | [wildfly-swarm/wildfly-swarm](https://github.com/wildfly-swarm/wildfly-swarm) |
| Wildfly | WFARQ | [WFARQ.tar](https://sourceforge.net/projects/irblsensitivity/files/Wildfly/WFARQ.tar) | [wildfly/wildfly-arquillian](https://github.com/wildfly/wildfly-arquillian) |
| Wildfly | WFCORE | [WFCORE.tar](https://sourceforge.net/projects/irblsensitivity/files/Wildfly/WFCORE.tar) | [wildfly/wildfly-core](https://github.com/wildfly/wildfly-core) |
| Wildfly | WFLY | [WFLY.tar](https://sourceforge.net/projects/irblsensitivity/files/Wildfly/WFLY.tar) | [wildfly/wildfly](https://github.com/wildfly/wildfly) |
| Wildfly | WFMP | [WFMP.tar](https://sourceforge.net/projects/irblsensitivity/files/Wildfly/WFMP.tar) | [wildfly/wildfly-maven-plugin](https://github.com/wildfly/wildfly-maven-plugin) |
| Spring | AMQP | [AMQP.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/AMQP.tar) | [spring-projects/spring-amqp](https://github.com/spring-projects/spring-amqp) |
| Spring | ANDROID | [ANDROID.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/ANDROID.tar) | [spring-projects/spring-android](https://github.com/spring-projects/spring-android) |
| Spring | BATCH | [BATCH.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/BATCH.tar) | [spring-projects/spring-batch](https://github.com/spring-projects/spring-batch) |
| Spring | BATCHADM | [BATCHADM.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/BATCHADM.tar) | [spring-projects/spring-batch-admin](https://github.com/spring-projects/spring-batch-admin) |
| Spring | DATACMNS | [DATACMNS.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/DATACMNS.tar) | [spring-projects/spring-data-commons](https://github.com/spring-projects/spring-data-commons) |
| Spring | DATAGRAPH | [DATAGRAPH.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/DATAGRAPH.tar) | [spring-projects/spring-data-neo4j](https://github.com/spring-projects/spring-data-neo4j) |
| Spring | DATAJPA | [DATAJPA.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/DATAJPA.tar) | [spring-projects/spring-data-jpa](https://github.com/spring-projects/spring-data-jpa) |
| Spring | DATAMONGO | [DATAMONGO.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/DATAMONGO.tar) | [spring-projects/spring-data-mongodb](https://github.com/spring-projects/spring-data-mongodb) |
| Spring | DATAREDIS | [DATAREDIS.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/DATAREDIS.tar) | [spring-projects/spring-data-redis](https://github.com/spring-projects/spring-data-redis) |
| Spring | DATAREST | [DATAREST.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/DATAREST.tar) | [spring-projects/spring-data-rest](https://github.com/spring-projects/spring-data-rest) |
| Spring | LDAP | [LDAP.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/LDAP.tar) | [spring-projects/spring-ldap](https://github.com/spring-projects/spring-ldap) |
| Spring | MOBILE | [MOBILE.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/MOBILE.tar) | [spring-projects/spring-mobile](https://github.com/spring-projects/spring-mobile) |
| Spring | ROO | [ROO.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/ROO.tar) | [spring-projects/spring-roo](https://github.com/spring-projects/spring-roo) |
| Spring | SEC | [SEC.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SEC.tar) | [spring-projects/spring-security](https://github.com/spring-projects/spring-security) |
| Spring | SECOAUTH | [SECOAUTH.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SECOAUTH.tar) | [spring-projects/spring-security-oauth](https://github.com/spring-projects/spring-security-oauth) |
| Spring | SGF | [SGF.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SGF.tar) | [spring-projects/spring-data-gemfire](https://github.com/spring-projects/spring-data-gemfire) |
| Spring | SHDP | [SHDP.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SHDP.tar) | [spring-projects/spring-hadoop](https://github.com/spring-projects/spring-hadoop) |
| Spring | SHL | [SHL.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SHL.tar) | [spring-projects/spring-shell](https://github.com/spring-projects/spring-shell) |
| Spring | SOCIAL | [SOCIAL.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SOCIAL.tar) | [spring-projects/spring-social](https://github.com/spring-projects/spring-social) |
| Spring | SOCIALFB | [SOCIALFB.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SOCIALFB.tar) | [spring-projects/spring-social-facebook](https://github.com/spring-projects/spring-social-facebook) |
| Spring | SOCIALLI | [SOCIALLI.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SOCIALLI.tar) | [spring-projects/spring-social-linkedin](https://github.com/spring-projects/spring-social-linkedin) |
| Spring | SOCIALTW | [SOCIALTW.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SOCIALTW.tar) | [spring-projects/spring-social-twitter](https://github.com/spring-projects/spring-social-twitter) |
| Spring | SPR | [SPR.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SPR.tar) | [spring-projects/spring-framework](https://github.com/spring-projects/spring-framework) |
| Spring | SWF | [SWF.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SWF.tar) | [spring-projects/spring-webflow](https://github.com/spring-projects/spring-webflow) |
| Spring | SWS | [SWS.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SWS.tar) | [spring-projects/spring-ws](https://github.com/spring-projects/spring-ws) |
| Previous | AspectJ | [AspectJ.tar](https://sourceforge.net/projects/irblsensitivity/files/Previous/AspectJ.tar) | [eclipse/org.aspectj](https://github.com/eclipse/org.aspectj) |
| Previous | JDT | [JDT.tar](https://sourceforge.net/projects/irblsensitivity/files/Previous/JDT.tar) | [eclipse/eclipse.jdt.core](https://github.com/eclipse/eclipse.jdt.core) |
| Previous | PDE | [PDE.tar](https://sourceforge.net/projects/irblsensitivity/files/Previous/PDE.tar) | [eclipse/eclipse.pde.ui](https://github.com/eclipse/eclipse.pde.ui) |
| Previous | SWT | [SWT.tar](https://sourceforge.net/projects/irblsensitivity/files/Previous/SWT.tar) | [eclipse/eclipse.platform.swt](https://github.com/eclipse/eclipse.platform.swt) |
| Previous | ZXing | [ZXing.tar](https://sourceforge.net/projects/irblsensitivity/files/Previous/ZXing.tar) | [zxing/zxing](https://github.com/zxing/zxing) |

## Citing

This document describes how to use this dataset and how to reproduce the result of our paper below. Please cite the following paper if you utilize the dataset:

```
@inproceedings{bench4bl,
  Author = {Jaekwon Lee and Dongsun Kim and Tegawend\'e F. Bissyand\'e and Woosung Jung and Yves Le Traon},
  Title = {Bench4BL: Reproducibility Study of the Performance of IR-based Bug Localization},
  Booktitle = {Proceedings of the 27th ACM SIGSOFT International Symposium  on  Software Testing and Analysis},
  Series = {ISSTA 2018},
  Year = {2018},
  doi = {10.1145/3213846.3213856},
  pages = {1--12}
}
```

---

### Download subjects' archives.
Download all subjects from the Subjects table and save them in the cloned repository path. We saved them into the 'Bench4BL/archives' directory. To use our scripts, we recommend that each subject stores in the group directory to which it belongs. After downloaded, unpack all archives by using the unpacking.sh script. If you don't need all subjects, you can download some of them.

```sh
$ cd Bench4BL
Bench4BL$ mkdir archives
Bench4BL$ cd archives
Bench4BL/archives$ mkdir Apache 
Bench4BL/archives$ cd Apache
Bench4BL/archives/Apache$ wget -O CAMEL.tar "https://sourceforge.net/projects/irblsensitivity/files/Apache/CAMEL.tar"
....work recursively....
Bench4BL$ mkdir data
Bench4BL$ chmod +x unpacking.sh
Bench4BL$ ./unpacking.sh archives data
```

The last command unpacks all archive files in `archives` folder into 'data' folder as keeping the directory structures in `archives`.

We appended the script to download all archives to the `archives` folder. If you want to use this, please use following instructions. This scripts creats all folders and download archives into each folder.

```sh
$ chmod +x downloads.sh
$ ./downloads.sh
```

### Version Information
We selected specific versions for each subject and saved into 'versions.txt'. The file is in JSON format and we used a dictionary to save information. Top-level keys mean a subject name corresponding to "Subjects.py". The selected versions are also listed in dictionary structure. The key text is version name which means you want to represent it and the value test is tag name written in git repository.
For example, assume that you want to store CODEC Subject's version information. You prepare JSON code and save it in 'Bench4BL/data/Commons/CODEC/versions.txt'. We offer the selected versions in the archieves. If you want to use a version that we selected, it is not necessary to change version information files.

```
{
    "CODEC":{
            "1.4":"CODEC_1_4",
            "1.5":"commons-codec-1.5",
            "1.6":"1_6",
            "1.7":"1.7",
            "1.1":"CODEC_1_1",
            "1.2":"CODEC_1_2",
            "1.3":"CODEC_1_3",
            "1.8":"1.8",
            "1.9":"1.9",
            "1.10":"1.10"
    }
}
```
