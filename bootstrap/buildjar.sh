#!/bin/sh

# cd `git rev-parse --show-toplevel`/src/Locus
# mvn package -DskipTests -fn
# cp target/Locus.jar ../../techniques

cd `git rev-parse --show-toplevel`/src/BugLocator
mvn package  -DskipTests -fn
cp target/BugLocator.jar ../../techniques

# cd `git rev-parse --show-toplevel`/src/AmaLgam
# mvn package  -DskipTests -fn
# cp target/AmaLgam.jar ../../techniques

# cd `git rev-parse --show-toplevel`/src/BLUiR
# mvn package  -DskipTests -fn
# cp target/BLUiR.jar ../../techniques

cd `git rev-parse --show-toplevel`/src/BRTracer
mvn package  -DskipTests -fn
cp target/BRTracer.jar ../../techniques
