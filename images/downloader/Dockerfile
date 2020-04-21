FROM registry.redhat.io/rhel7
COPY yum.conf /etc/yum.conf
CMD yum clean metadata
ENTRYPOINT ["yumdownloader","-d 5","-e 5","--destdir","/var/cache/yum/x86_64/7Server/"]


