#!/bin/bash

s3_bucket=%1
dest_folder=%2

echo " aws s3 sync $s3_bucket $dest_folder "
aws s3 sync $s3_bucket $dest_folder
