#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

from stage.service.service import StageServer

if len(sys.argv) != 2:
    sys.exit('Syntax: %s COMMAND' % sys.argv[0])

cmd = sys.argv[1].lower()
# initialize staging server
service = StageServer(name='iris_staging_server', pid_dir='/tmp')

if cmd == 'start':
    print("Starting service.")
    service.start()
elif cmd == 'stop':
    print("Stopping service.")
    service.stop()
else:
    sys.exit('Unknown command "%s".' % cmd)
