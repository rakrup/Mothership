
#AWS setup for boto
import boto3
from botocore.exceptions import ClientError
# GCP set up 
from pprint import pprint
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import os
import json
import digitalocean
#
# GET Session Credentials stored in 
# ~/.aws/credentials in Environment Variables 
# (AWS_ACCESS_KEY_ID , AWS_SECRET_ACCESS_KEY)
#

# Get Session (based on profile in ~/.aws/credentails ,
# Using default profile

# using Service Acount Credentials and setting GOOGLE_APPLICATION_CREDENTIALS credentials 
#to the json file containing credentials details


# expects ami Id as input ami is of string type
def tagAWSami(ami):
	sess=boto3.Session()
	ec2Client=sess.resource('ec2')
	image=ec2Client.Image(ami)
	try:
       		image.create_tags(\
			Tags=[\
 				{\
  				'Key':'status',\
  				'Value':'vulnerable',\
 				}\
			]\
		)
		#print image.tags
	except ClientError as e:
     		print "Image Not Found"
	return

# expects img id as input and type is of string
def tagGCPImg(img):
         
	os.environ['GOOGLE_APPLICATION_CREDENTIALS']="/Users/gauravsingh/Documents/2712reiminder-0ce115eb71b6.json"
	g_credentials = GoogleCredentials.get_application_default()
	g_service = discovery.build('compute', 'v1', credentials=g_credentials)
	data = json.load(open(os.environ['GOOGLE_APPLICATION_CREDENTIALS']))
	project=data.get('project_id')
    	try:	
        	request=g_service.images().get(project=project, image=img)
        	response=request.execute()
        	#pprint(response)
		labels_request_body = {
           	"labels":{
              		"status":"vulnerable",
           	},
           	"labelFingerprint": response.get('labelFingerprint'),
		}	

		request = g_service.images().setLabels(project=project, resource=img, body=labels_request_body)
		response = request.execute()

   	except  :
                print "Image not found"

# expects droplet id as input and it should be of string type 
def tagdigitDroplet(drop_id):       
	os.environ['DIGITAL_KEY']="/Users/gauravsingh/Documents/digitaltoken.txt"
	access_key=""
	f = open(os.environ['DIGITAL_KEY'], 'r')
        for line in f:
            access_key=line[:-1]
        f.close()
        print access_key
        tag = digitalocean.Tag(token=access_key, name="vulnerable")
        tag.create()
        try:
            tag.add_droplets([drop_id])
        except :
            print "Drop id is incorrect"


#tagAWSami('ami-264f5c5c')
#tagGCPImg("image-121")
#tagdigitDroplet("82260821")
