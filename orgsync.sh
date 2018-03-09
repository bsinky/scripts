#!/usr/bin/env bash

# Script to sync org-mode files stored in the home directory to cloude storage.
#
# *nix version

now=`date '+%Y_%m_%d_%H_%M_%S'`
logdir="$HOME/orglogs/"
logfile="$logdir$now.log"

# Ensure logdir directory exists
mkdir -p $logdir

# create empty logfile
touch $logfile

orgdir="$HOME/org"

rclone copy google:org $orgdir -v -u --log-file $logfile
rclone sync $orgdir google:org -v -u --log-file $logfile
