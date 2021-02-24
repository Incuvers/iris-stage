#!/usr/bin/python3
# -*- coding: utf-8 -*-

from stage.aws.sqs import SQSClient

SQSClient().poll_sqs()
