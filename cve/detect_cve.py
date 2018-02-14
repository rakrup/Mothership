import os
import re
import csv
import click
import json
import sys
parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name+"/db")
sys.path.append(parent_dir_name+"/taggingScript")
from ares import CVESearch
from collections import defaultdict
import sqlite3
import py_sqlite
import tagImages

var=sys.argv[1]
b_id=var.split("/")[1]
print b_id
query="select ami_id from packer_run where build_no='"+b_id+"'"

c_query = "create table if not exists cve_details(build_no string,CVE string, package string,ptime string,updated_ts DATETIME DEFAULT CURRENT_TIMESTAMP)"
db_name="db/packerDB.db"

py_sqlite.db_create(db_name,c_query)
ami=py_sqlite.db_select1(db_name,query)
print ami
#exit(0)
PRIORITY_PATTERNS = {
    'low': re.compile('Priority:'),
    'medium': re.compile('Priority: [mh]'),
    'high': re.compile('Priority: [h]'),
}
CVE = CVESearch()

CVE_DETAILS_TEMPLATE = """
CVE: {id}, Package: {package},CVSS: {cvss},Published: {published},Modified: {modified}
"""
CVE_NO_DETAILS_TEMPLATE = """
CVE: {id}
Package: {package}
No further details available.
"""

@click.command()
@click.argument('packages_listing', type=click.File('rb'))
@click.argument('active_cve_directory', type=click.Path(exists=True, dir_okay=True, file_okay=False))
@click.option('--ubuntu-version', default='xenial')
@click.option('--priority-threshold', default='medium', type=click.Choice(PRIORITY_PATTERNS.keys()))
@click.option('--any-status', is_flag=True)
def scan_packages(packages_listing, active_cve_directory, ubuntu_version, priority_threshold, any_status):
    cves = load_cves(active_cve_directory, ubuntu_version, priority_threshold)
    next(packages_listing) # remove header
    cve_counter = 0
    for package_line in packages_listing:
        package, _, _ = package_line.partition(b'/')
        package = package.decode('utf-8')
	#print package
        if package in cves:
            cve_counter = cve_counter + 1
            output_details(package, cves[package], any_status)
    print cve_counter
    if cve_counter > 0:
        tagImages.tagAWSami(ami)

def output_details(package, cves, any_status=False):
    for cve, status in cves:
        if any_status:
            print_cve(cve, package)
        elif 'need' in status:
            print_cve(cve, package)

def print_cve(cve, package):
    details = json.loads(CVE.id(cve).decode("utf-8") )
    #print details
    if details:
        print(CVE_DETAILS_TEMPLATE.format(
            id=cve,
            package=package,
            cvss=details['cvss'],
            published=details['Published'],
            modified=details['Modified']
            #summary=details['summary'],
            #references=' '.join(details['references'])
        ))
        query = "INSERT INTO cve_details(build_no,CVE, package,ptime) VALUES('"+b_id+"','"+cve+"','"+package+"','"+details['Published']+"')"
        #print query
        py_sqlite.db_insert(db_name,query)
        #db_insert(query)
    else:
        print(CVE_NO_DETAILS_TEMPLATE.format(id=cve, package=package))


def load_cves(active_cve_directory, ubuntu_version, threshold):
    cves = defaultdict(list)
    package_regex = re.compile('{}_(?P<package_name>[\w_-]*): (?P<status>\w*)'.format(ubuntu_version))
    for filename in filter(lambda fn: fn.startswith('CVE'), os.listdir(active_cve_directory)):
        with open(os.path.join(active_cve_directory, filename)) as f:
            contents = f.read()
            matches = []
            if re.search(PRIORITY_PATTERNS[threshold], contents) != None:
                matches = re.finditer(package_regex, contents)
            for match in matches:
                match_dict = match.groupdict()
                cves[match_dict['package_name']].append((filename, match_dict['status']))
    return cves


if __name__=='__main__':
	scan_packages()
