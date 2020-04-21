FROM registry.redhat.io/rhel7
RUN yum install -y python3 && pip3 install redis
COPY parse.py /
ENTRYPOINT ["python3","-u","/parse.py"] 

