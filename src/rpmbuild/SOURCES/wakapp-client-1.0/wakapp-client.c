#include<stdlib.h>
#include<stdio.h>

  main() {
    int ret;
    ret=system("id wakausr &>/dev/null");
    if (!ret) {
                printf("\nERR: waka user seems to be present from a previous installation; kindly remove it with 'userdel -r wakausr' and reinstall the package\n");
                return; 
              }
    system("groupadd wakausr &>/dev/null");
    ret=system("useradd wakausr -g wakausr &>/dev/null && mkdir /home/wakausr/.ssh && ssh-keygen -f /home/wakausr/.ssh/id_rsa -P '' &>/dev/null"); 
    if (ret)
                printf("\nERR: an error occured either adding waka user or creating its home directory\n");
    else {
                system("echo 'sshpubkey' 2>/dev/null >/home/wakausr/.ssh/authorized_keys");
                system("chown -R wakausr.wakausr /home/wakausr/.ssh &&  chmod 700 /home/wakausr/.ssh && restorecon -FR /home/wakausr/.ssh");
    } 

    system("echo 'wakausr ALL=(ALL) NOPASSWD:ALL' >/etc/sudoers.d/wakausr");

  }

