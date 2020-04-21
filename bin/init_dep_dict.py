#!/usr/bin/env python3
import sys
import redis
import json

print('Starting ...')

conn = redis.Redis('localhost')

with open('./pkg_dep.json','r') as f:
 data=json.load(f)

#serialize
conn.set("rhel7_dep_dict",json.dumps(data))

print('Done.')

