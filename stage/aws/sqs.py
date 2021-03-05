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

class SQSClient:

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        # Create SQS client
        self.sqs = boto3.client('sqs')
        # Latch on available SQS queue
        response = self.sqs.list_queues()
        self.logger.info("SQS Queue list: %s", response['QueueUrls'])
        self.sqs_queue_url=response['QueueUrls'][-1]
        self.logger.info("%s instantiated successfully.", __name__)

    def poll_sqs(self) -> bool:
        """
        Polls SQS server for snap push completion messages.

        :returns: True if SQS poll returns a notification and False otherwise
        """
        # Receive message from SQS queue
        try:
            response = self.sqs.receive_message(
                QueueUrl=self.sqs_queue_url,
                AttributeNames=[
                    'SentTimestamp'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ],
                VisibilityTimeout=0,
                WaitTimeSeconds=20
            )
        except BaseException as exc:
            self.logger.exception(
                "An exception occured when making sqs request: %s", exc)
            return False
        
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
                QueueUrl=self.sqs_queue_url,
                ReceiptHandle=receipt_handle
            )
            return True
        return False
