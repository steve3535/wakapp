#!/usr/bin/env python
import pika
import docker
import os
import sys 
import subprocess
import threading

def process_download(body):
 client = docker.from_env()
 container = client.containers.run("docker.io/nigelfoster/rhel-proxy:7c",body,
                        volumes={'/etc/yum.repos.d/': {'bind':'/etc/yum.repos.d/', 'mode':'ro'},
                                 '/etc/pki/entitlement/': {'bind':'/etc/pki/entitlement/','mode':'ro'},
                                 '/media7/': {'bind':'/media7/','mode':'ro'},
                                 '/media6/': {'bind':'/media6/','mode':'ro'},
                                 '/var/cache/yum/x86_64/7Server/stream7/': {'bind':'/var/cache/yum/x86_64/7Server/','mode':'rw'}},
                                 detach=True,remove=False)
 print(" [x] %s" % container.id )
 while(True):
  container.reload()
  if container.status == 'exited' :
     break


def data_handler(ch, method, properties,body):
 print(" [x] Received %r" % body)
 strarg=''.join(body)
 #print(strarg)
 thread = threading.Thread(target=process_download,args=(strarg,))
 thread.start()
 while thread.is_alive():  
    ch._connection.sleep(1.0)
 print(" [X] Done")
 ch.basic_ack(delivery_tag = method.delivery_tag)

def main():
 f = open("./fetch_main.log",'a')
 #sys.stdout = f
 #sys.stderr = f
 pid=os.getpid()
 dirname="/var/cache/yum/x86_64/7Server/stream7/{}".format(pid)
 connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
 channel = connection.channel()
 channel.queue_declare(queue='yum')
 channel.basic_qos(prefetch_count=1) 
 channel.basic_consume(queue='yum',on_message_callback=data_handler)
 print(' [*] Waiting for messages. To exit press CTRL+C')
 try:
  channel.start_consuming()
 except KeyboardInterrupt:
  channel.stop_consuming()
 channel.close()

if __name__ == '__main__':
    main()
