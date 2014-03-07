#!/usr/bin/python

import sys


command = "lsof +c 0 -n -i -P | awk '{ print $1 " " $5  " " $8 " " $9 " " $10}'"
