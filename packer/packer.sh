#/bin/bash
COCKPIT='/home/rahul/Mothership'
PACKERCONFIG=$1
UUID=`uuidgen`
LOGFILE=$COCKPIT/log/$UUID.log
OUTPUTDIR=$COCKPIT/output/$UUID
source $COCKPIT/creds/aws.creds
ACCOUNT_FILE=$COCKPIT/creds/account.json
source $COCKPIT/creds/DO.creds
TIME=`date +%D-%H:%M:%S`
ANSIBLE_LOCATION=$COCKPIT/packer/ansible/apache/apache.yml
ANSIBLE_EXTRA_VARS='["--extra-vars","ansible_sudo_pass=rahul"]'

touch "$LOGFILE"
echo "Starting a build with Build-ID : $UUID"
echo "Tail the logs at $LOGFILE for more details.."
packer build  -var "aws_access_key=$AWS_ACCESS_KEY" -var "aws_secret_key=$AWS_SECRET_KEY" -var "google_account_file=$ACCOUNT_FILE" \
       -var "digitalocean_api_key=$DO_API_KEY"	-var "ansible_location=$ANSIBLE_LOCATION" \
       -var "ansible_extra_params=$ANSIBLE_EXTRA_VARS=" $PACKERCONFIG > $LOGFILE
AMI=`grep ami $LOGFILE  | grep west| grep -v ec2  | awk -F':' '{print $2}'`
DOI=`grep digitalocean $LOGFILE| grep snapshot |grep created | awk -F "'" '{print $2}'`
GCP=`grep googlecompute $LOGFILE| grep 'disk image was created' | awk -F ":" '{print $3}'`

echo "--------------------------------------"
echo "|             Build Result           | "
echo "--------------------------------------"
echo "|UUID         | $UUID "
echo "|AMI-id       | $AMI"
echo "|Digital Ocean| $DOI"
echo "|Google CLoud | $GCP"
echo "--------------------------------------"
echo "Copy of result also present in the $OUTPUTDIR"

mkdir -p $OUTPUTDIR
echo "BUILD START TIME : $TIME" >> $OUTPUTDIR/build.result
echo "UUID : $UUID" >> $OUTPUTDIR/build.result
echo "AMI : $AMI" >> $OUTPUTDIR/build.result
echo "DigitalOcean : $DOI" >> $OUTPUTDIR/build.result
echo "GoogleCloud : $GCP" >> $OUTPUTDIR/build.result

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
/usr/bin/python $SCRIPT_DIR/packer_db_helper.py $UUID $TIME $AMI $GCP 

cp package.list $OUTPUTDIR/package.list
rm package.list
