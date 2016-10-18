#!/bin/bash

workdir=`dirname $0`
cd ${workdir}
workdir=`pwd`

echo ${workdir}

export GOPATH=${workdir}

go build -o seq ./src
