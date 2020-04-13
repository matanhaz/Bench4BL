#!/bin/sh

cd `git rev-parse --show-toplevel`/src/Locus
mvn package
cp target/Locus.jar ../../techniques

cd `git rev-parse --show-toplevel`/src/BugLocator
mvn package
cp target/BugLocator.jar ../../techniques

cd `git rev-parse --show-toplevel`/src/AmaLgam
mvn package
cp target/AmaLgam.jar ../../techniques

cd `git rev-parse --show-toplevel`/src/BLUiR
mvn package
cp target/BLUiR.jar ../../techniques

cd `git rev-parse --show-toplevel`/src/BRTracer
mvn package
cp target/BRTracer.jar ../../techniques
