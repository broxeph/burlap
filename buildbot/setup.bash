#!/bin/bash
# Creates a local PIP-aware shell.
#set -e
if [ $_ == $0 ]
then
    echo "Please source this script. Do not execute."
    exit 1
fi
#script_dir=`dirname $0`
#cd $script_dir
. ../.env/bin/activate
PS1="\u@\h:\W(virt)\$ "