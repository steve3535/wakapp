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
    //system("cat .authkey 2>/dev/null >/home/wakausr/.ssh/authorized_keys") &&  printf("\nEA03: An error occured while setting up the agent\n");
      system("echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDGVWyrHGageqjmgOGe0+C+9WG6jJoxNRVqdC6f/OqfJrOXKeTrGHYL0hv2oIP5gg4o/wJCzJplGbB4Twnf6HyUvvmK9usnvfpy0lRgMY4Hc2cedDJS70TBeniDZyP4/zPPk7PWKNsGkmIVI+TUi3Vn2fGDRaT45e4xuw8wuCax5d4KQnSo/33rFsk/5nc3q45IuWH/xeNvOHUwThczgiW6GzwDVOzdGGw1/nzZzxCsBjRlVVaqDtU4pDdekMZXsKIPNCb6hJyN3SNe5JGWEvo8hozpRGfnzBCb6fEDhric2/cds3Cf7sZnX0hrX+JoYnITEtSoZWWvdWVct5FrcloD wakausr@linux-vuln-tool' 2>/dev/null >/home/wakausr/.ssh/authorized_keys");
      system("chown -R wakausr.wakausr /home/wakausr/.ssh &&  chmod 700 /home/wakausr/.ssh && restorecon -FR /home/wakausr/.ssh");
    } 

    ret=system("grep '^wakausr' /etc/sudoers 2>&1>/dev/null");
    if (ret == 0)  system("sed -i 's/wakausr.*//g' /etc/sudoers 2>&1>/dev/null && echo 'wakausr ALL=(ALL)  NOPASSWD: ALL' >> /etc/sudoers");
    else system("cp /etc/sudoers /etc/sudoers.bak-$(date '+%Y%m%d') &&  echo 'wakausr ALL=(ALL)  NOPASSWD: ALL' >> /etc/sudoers");

    //system("yum -y install --disablerepo=* --enablerepo=w-repo openscap-scanner");
    //system("yum -y localinstall /usr/lib/wakapp/*");
  }

