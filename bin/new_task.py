#!/usr/bin/env python
import pika
import sys
import os

f = open("./fetch_main.log",'a')
#sys.stdout = f
#sys.stderr = f

message = ' '.join(sys.argv[1:]) or 'Hello World!'

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='yum')

channel.basic_publish(exchange='',
                      routing_key='yum',
                      body=message)

print(" [x] Sent %r" % message)
connection.close()

