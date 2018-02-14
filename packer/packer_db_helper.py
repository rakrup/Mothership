import sys
import os
parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name+"/db")
import sqlite3
import py_sqlite

# Create the table in database
c_query = "create table if not exists packer_run(build_no string,build_time string, ami_id string,gcloud_id string,updated_ts DATETIME DEFAULT CURRENT_TIMESTAMP)"
db_name=parent_dir_name+"/db/"+"packerDB.db"
py_sqlite.db_create(db_name,c_query)


# Create the query and push to database
query = "INSERT INTO packer_run(build_no,build_time,ami_id,gcloud_id) VALUES('" + sys.argv[1] + "' ,'"+ sys.argv[2] +"','"+ sys.argv[3] + "','" + sys.argv[4] +"')"
py_sqlite.db_insert(db_name,query)


