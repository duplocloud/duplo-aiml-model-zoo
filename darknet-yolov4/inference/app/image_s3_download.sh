#!/bin/bash

s3_bucket=$1
dest_folder=$2

#containers outside duplo  -- /root/.aws/crendential
#this file can not access /root/.aws === as nginx is running with nginx user  not root
#export AWS_ACCESS_KEY_ID=a
#export AWS_SECRET_ACCESS_KEY=b
#export AWS_DEFAULT_REGION=us-west-2

echo "======== downloading:  aws s3 cp $s3_bucket $dest_folder "
aws s3 cp $s3_bucket $dest_folder
sleep 1
ls -alt $dest_folder