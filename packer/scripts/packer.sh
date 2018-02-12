
packer build  -var 'aws_access_key=AKIAJK33DVH3SS6YNJXQ' -var 'aws_secret_key=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' packerex.json > packer_logs.txt
AMI=`grep ami packer_logs.txt  | grep west| grep -v ec2  | awk -F':' '{print $2}'`
