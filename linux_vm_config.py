#!/usr/bin/env python
import os, re


def basic_config(hostname):
    cmd = '''echo 'alias vi="vim"' >> ~/.bashrc'''
    os.system(cmd)
    os.system('systemctl set-default multi-user.target')
    cmd = 'echo ' + hostname + ' >/etc/hostname'
    os.system(cmd)


def generate_nic_config(nic, ip):
    nic_conf_path = "/etc/sysconfig/network-scripts/"
    nic_conf = nic_conf_path + "ifcfg-" + nic

    config_str = "TYPE=Ethernet\n"
    config_str += "BOOTPROTO=static\n"
    config_str += "DEFROUTE=yes\n"
    config_str += "PEERDNS=yes\n"
    config_str += "PEERROUTES=yes\n"
    config_str += "NAME=" + nic + "\n"
    config_str += "DEVICE=" + nic + "\n"
    config_str += "ONBOOT=yes\n"
    config_str += "IPADDR=" + ip + "\n"
    config_str += "NETMASK=255.255.255.0\n"

    f = open(nic_conf, 'wb')
    f.write(config_str)
    f.close()


def network_config(ip):
    cmd = 'ip addr'
    output = os.popen(cmd).read()
    nic_list = re.findall(r': (ens[0-9]*):', output)
    for nic in nic_list:
        generate_nic_config(nic, ip)


def optical_disk_config():
    os.system("umount /dev/sr0")
    os.system("mkdir /mnt/cdrom")
    os.system("mount /dev/sr0 /mnt/cdrom")
    os.system("cat /proc/mounts |grep /dev/sr0 >> /etc/fstab")


def disabled_centos_repo(repo):
    cmd = 'sed -i "s/enabled=1/enabled=0/g" ' + repo
    print cmd
    os.system(cmd)


def generate_local_yum():
    yum_path = "/etc/yum.repos.d/yum_local.repo"
    config_str = "[local-os]\n"
    config_str += "name=local-os\n"
    config_str += "baseurl=file:///mnt/cdrom/\n"
    config_str += "gpgcheck=0\n"
    config_str += "enabled=1\n"

    f = open(yum_path, 'wb')
    f.write(config_str)
    f.close()


def yum_config():
    centos_repo_list = os.popen("ls /etc/yum.repos.d/CentOS-*.repo").readlines()
    for centos_repo in centos_repo_list:
        disabled_centos_repo(centos_repo)
    generate_local_yum()


if __name__ == '__main__':
    basic_config(hostname='docker_2')
    generate_nic_config("ens33", "192.168.204.12") #config the nic with ip
    optical_disk_config()
    yum_config()
    print('vm config successfully')

