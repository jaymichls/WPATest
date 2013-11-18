#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
for i in range(20):
	subprocess.call('airmon-ng stop mon%d'%(i),shell=True)
