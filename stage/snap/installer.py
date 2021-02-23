#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Snap Installer
==============
Modified: 2021-02

Handles new snap installations from s3 download location
"""
import os
import logging

class Installer:

    # bind logging to config file
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s"
    )

    def __init__(self) -> None:
        self.tmp = os.environ['SNAP_FP']
        self.name = os.environ['SNAP_NAME']
        logging.info("%s instantiated successfully.", __name__)

    def install(self):
        """
        """
        logging.info("")
        os.system(f"snap remove {self.name}")
        logging.info("Installing newest snap")
        os.system(f"snap install {self.tmp} --devmode")
        logging.info("Installing newest snap")