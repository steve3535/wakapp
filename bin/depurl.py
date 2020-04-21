import os
import redis
import json
import sys

conn = redis.Redis('localhost')
current = conn.get("yum7_dep_dict")
yum_dep_dict = json.loads(current)

file=sys.argv[1]
with open(file,'r') as f:
 contents = f.read()
 #yum_dep_dict=json.load(f)

for item in contents.split():
    if item in yum_dep_dict:
        print(item,yum_dep_dict[item])
    else:
        instruction='yumdownloader --resolve "+item+" --urls 2>/dev/null | egrep "installed|updated" | cut -d " " -f3 | cut -f1 -d.'
        stream = os.popen(instruction)
        data = stream.read()
        yum_dep_dict[item]=data
 
conn.set("yum7_dep_dict",json.dumps(yum_dep_dict))


