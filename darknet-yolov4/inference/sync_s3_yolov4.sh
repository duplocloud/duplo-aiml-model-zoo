#!/bin/bash

s3_bucket=$1
dest_folder=$2

echo " aws s3 sync $s3_bucket $dest_folder "

ls -alt $dest_folder
if test -f "$dest_folder/download_complete";
then
    echo " downloaded aws s3 sync $s3_bucket $dest_folder "
else
    echo " downloading aws s3 sync $s3_bucket $dest_folder ...."
    aws s3 sync $s3_bucket $dest_folder
    touch "$dest_folder/download_complete"
fi
ls -alt $dest_folder

