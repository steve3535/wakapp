#include<stdlib.h>
#include<stdio.h>

  main() {
    int ret;
    ret=system("id wakausr >/dev/null 2>&1");
    if (ret == 0){
      printf("\nEA01: Error: waka user seems to be present from a previous installation; kindly remove it with 'userdel -r wakausr' and reinstall the agent package\n");
      return; 
    }
    ret=system("useradd wakausr >/dev/null 2>&1 && mkdir /home/wakausr/.ssh && ssh-keygen -f /home/wakausr/.ssh/id_rsa -P '' >/dev/null 2>&1"); 
    if (ret != 0)
      printf("\nEA02: An error occured while installing the agent\n");
    else {
      system("echo 'sshpubkey' 2>/dev/null >/home/wakausr/.ssh/authorized_keys");
      system("chown -R wakausr.wakausr /home/wakausr/.ssh &&  chmod 700 /home/wakausr/.ssh && restorecon -FR /home/wakausr/.ssh");
    } 

    system("echo 'wakausr ALL=(ALL) NOPASSWD:ALL' >/etc/sudoers.d/wakausr");
    //ret=system("grep '^wakausr' /etc/sudoers 2>&1>/dev/null");
    //if (ret == 0)  system("sed -i 's/wakausr.*//g' /etc/sudoers 2>&1>/dev/null && echo 'wakausr ALL=(ALL)  NOPASSWD: ALL' >> /etc/sudoers");
    //else system("cp /etc/sudoers /etc/sudoers.bak-$(date '+%Y%m%d') &&  echo 'wakausr ALL=(ALL)  NOPASSWD: ALL' >> /etc/sudoers");

  }

