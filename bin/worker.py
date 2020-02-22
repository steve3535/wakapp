#!/usr/bin/env python
import pika
import docker
import os
import sys 
import subprocess

#f = open(os.devnull, 'w')
#sys.stdout = f
#sys.stderr = f

f = open("./fetch_main.log",'a')
sys.stdout = f
sys.stderr = f

pid=os.getpid()
dirname="/var/cache/yum/x86_64/7Server/stream7/{}".format(pid)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='yum')

def callback(ch, method, properties, body):
 print(" [x] Received %r" % body)
 client = docker.from_env()
 client.containers.run("rhel-proxy:7b",body,
                        volumes={'/etc/yum.repos.d/': {'bind':'/etc/yum.repos.d/', 'mode':'ro'},
                                 '/etc/pki/entitlement/': {'bind':'/etc/pki/entitlement/','mode':'ro'},
                                 '/media7/': {'bind':'/media7/','mode':'ro'},
                                 '/media6/': {'bind':'/media6/','mode':'ro'},
                                 '/var/cache/yum/x86_64/7Server/stream7/': {'bind':'/var/cache/yum/x86_64/7Server/','mode':'rw'}},
                                 detach=False,remove=True)
 print(" [x] Done")

 ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(
    #queue='yum', on_message_callback=callback, auto_ack=True)
    queue='yum', on_message_callback=callback)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()