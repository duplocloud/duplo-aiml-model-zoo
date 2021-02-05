#!/bin/bash

s3_bucket=$1
dest_folder=$2


echo "======== start sync_s3_yolov4 aws s3 cp $s3_bucket $dest_folder "
aws s3 sync $s3_bucket $dest_folder
ls -alt $dest_folder