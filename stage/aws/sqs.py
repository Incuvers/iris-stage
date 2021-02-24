#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
AWS S3 -> SQS Staging Server
============================
Modified: 2021-02

This module listens for new snap publishes on S3 and downloads and installs
these new updates

This module listens for an SQS message on a multi-part upload event completion.
This triggers the server to pull the .snap file from s3, remove the current 
snap and install the new snap file
"""


import boto3
import logging.config

from stage.aws.s3 import S3Client
from stage.snap.installer import Installer

class SQSClient:

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        # Create SQS client
        self.sqs = boto3.client('sqs')
        self.s3_client = S3Client()
        self.installer = Installer()
        self.logger.info("%s instantiated successfully.", __name__)

    def poll_sqs(self) -> None:
        """
        Polls SQS server for snap push completion messages.
        """
        # List SQS queues
        response = self.sqs.list_queues()
        self.logger.info("SQS Queue list: %s", response['QueueUrls'])
        sqs_queue_url=response['QueueUrls'][-1]

        while True:
            # Receive message from SQS queue
            response = self.sqs.receive_message(
                QueueUrl=sqs_queue_url,
                AttributeNames=[
                    'SentTimestamp'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ],
                VisibilityTimeout=0,
                WaitTimeSeconds=10
            )
            self.logger.info("Received Response: %s", response)
            try:
                message = response['Messages'][0]
            except KeyError:
                pass
            else:
                self.logger.info("Receiving and digesting message")
                # digest recieved message and launch a service
                receipt_handle = message['ReceiptHandle']
                # Delete received message from queue
                self.sqs.delete_message(
                    QueueUrl=sqs_queue_url,
                    ReceiptHandle=receipt_handle
                )
                self.logger.info("Pulling recent snap from s3 bucket.")
                self.s3_client.pull()
                self.logger.info("Installing pulled snap.")
                self.installer.install()
                self.logger.info("Snap install complete.")
