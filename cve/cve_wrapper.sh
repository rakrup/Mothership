#!/bin/bash
ami=$1
echo $ami
r=$(sqlite3 db/packerDB.db "select build_no from packer_run where ami_id='$ami';")
echo $r
python cve/detect_cve.py output/$r/package.list ./ubuntu-cve-tracker/active --ubuntu-version=trusty
