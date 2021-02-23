#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
AWS S3 -> SQS Staging Server
============================
Modified: 2021-02

This module listens for new snap publishes on S3 and downloads and installs
these new updates

This module listens for an SQS message on a multi-part upload event completion.
This triggers the server to pull the .snap file from s3, remove the current snap and install the new snap file
"""

import boto3
import logging

class SQSClient:

    # bind logging to config file
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s"
    )

    def __init__(self) -> None:
        # Create SQS client
        sqs = boto3.client('sqs')
        logging.info("%s instantiated successfully.", __name__)

    # List SQS queues
    response = sqs.list_queues()
    logging.info("SQS Queue list: %s", response['QueueUrls'])
    sqs_queue_url=response['QueueUrls'][-1]

    while True:
        # Receive message from SQS queue
        response = sqs.receive_message(
            QueueUrl=sqs_queue_url,
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0,
            WaitTimeSeconds=5
        )
        logging.info("Received Response: %s", response)
        try:
            message = response['Messages'][0]
        except KeyError:
            logging.info("No message received")
        else:
            # digest recieved message and launch a service
            receipt_handle = message['ReceiptHandle']
            # Delete received message from queue
            sqs.delete_message(
                QueueUrl=sqs_queue_url,
                ReceiptHandle=receipt_handle
            )
            logging.info("Received and deleted message: %s", message)



`