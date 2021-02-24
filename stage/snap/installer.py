#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Snap Installer
==============
Modified: 2021-02

Handles new snap installations from s3 download location
"""
import os
import shutil
import logging.config

class Installer:

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.tmp = os.environ['SNAP_FP']
        self.name = os.environ['SNAP_NAME']
        self.secrets = os.environ['SNAP_SECRETS']
        self.common = os.environ['SNAP_COMMON']
        self.logger.info("%s instantiated successfully.", __name__)

    def install(self):
        """
        Uninstall existing snap, artificially inject machine secrets from
        secrets to $SNAP_COMMON and install new snap file in devmode.
        """
        os.system(f"snap remove {self.name}")
        self.logger.info("Installing newest snap")
        shutil.copytree(self.secrets, self.common)
        os.system(f"snap install {self.tmp} --devmode")
        self.logger.info("Installing newest snap")