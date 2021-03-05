#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
IRIS Staging Server Service
===========================
Modified: 2021-03


"""

import logging.config
import time

from service import Service
from stage.aws.s3 import S3Client
from stage.aws.sqs import SQSClient
from stage.snap.installer import Installer


class StageServer(Service):

    POLL_RATE = 5

    def __init__(self, name:str, pid_dir:str):
        self.logger = logging.getLogger(__name__)
        super().__init__(name, pid_dir)
        self.sqs_client = SQSClient()
        self.s3_client = S3Client()
        self.installer = Installer()
        self.logger.info("%s instantiated successfully.", __name__)

    def run(self) -> None:
        """
        Service runner entry and polling loop.
        """
        while not self.got_sigterm():
            response = self.sqs_client.poll_sqs()
            # pull snap from s3 and install if sqs poll yeilds notification
            if response:
                self.s3_client.pull()
                self.installer.install()
            time.sleep(self.POLL_RATE)