#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import logging.config

from iris_stage.service.service import StageServer

logger = logging.getLogger(__name__)
SERVICE_NAME = os.environ['SERVICE_NAME']
PID_DIR = os.environ['PID_DIR']

if len(sys.argv) != 2:
    sys.exit('Syntax: %s COMMAND' % sys.argv[0])

cmd = sys.argv[1].lower()
# instantiate staging server
service = StageServer(name=SERVICE_NAME, pid_dir=PID_DIR)

if cmd == 'start':
    logger.info("Starting %s service in %s", SERVICE_NAME, PID_DIR)
    service.start()
elif cmd == 'stop':
    logger.info("Halting %s service in %s", SERVICE_NAME, PID_DIR)
    service.stop()
else:
    sys.exit('Unknown command "%s".' % cmd)