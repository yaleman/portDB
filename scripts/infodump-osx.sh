#!/bin/bash
sudo lsof +c 0 -n -i -P | awk '{ print $1 " " $5  " " $8 " " $9 " " $10}' 