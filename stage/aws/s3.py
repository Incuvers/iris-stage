#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
S3 Client
=========
Modified: 2020-02

Pulls bucket objects from target s3 bucket
"""

import os
import boto3
import logging

class S3Client:

    bucket = os.environ['S3_BUCKET']
    obj = os.environ['S3_OBJECT']
    tmp = os.environ['SNAP_FP']

    def __init__(self) -> None:
        # here we need to get the bucket credentials from .aws/config so the 
        # aws credentials can be easily referenced and persist through service
        # restarts
        self.logger = logging.getLogger(__name__)
        self.s3 = boto3.client("s3")
        self.logger.info("%s instantiated successfully.", __name__)
    
    def pull(self) -> None:
        """
        Pulls file from target s3 bucket to /tmp
        """
        self.logger.info("Pulling %s from S3 %s bucket", self.obj, self.bucket)
        self.s3.download_file(self.bucket, self.obj, self.tmp)
        self.logger.info("S3 download complete.")