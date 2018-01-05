#!/usr/bin/env python
import os

DIR_PROXYCHAINS = "/root/.proxychains/"
PROXYCHAINS_PATH = DIR_PROXYCHAINS + "proxychains.conf"

# ------------- NEED TO CONFIG -----------------------
PROXY_IP = "192.168.3.106"
PROXY_PORT = "1088"
# ----------------------------------------------------

DOCKER_SERVICE_PATH = "/etc/systemd/system/docker.service.d/"
HTTP_PROXY_PATH = DOCKER_SERVICE_PATH + "http-proxy.conf"
HTTPS_PROXY_PATH = DOCKER_SERVICE_PATH + "https-proxy.conf"


def pc_config():
    """
    proxychains setup for the terminal command
    :return:
    """
    os.system("mkdir -p " + DIR_PROXYCHAINS)
    os.system("rm -rf " + PROXYCHAINS_PATH)
    pc_config = "strict_chain\n"
    pc_config += "proxy_dns\n"
    pc_config += "remote_dns_subnet 224\n"
    pc_config += "tcp_read_time_out 15000\n"
    pc_config += "tcp_connect_time_out 8000\n"
    pc_config += "localnet 127.0.0.0/255.0.0.0\n"
    pc_config += "quiet_mode\n\n"
    pc_config += "[ProxyList]\n"
    pc_config += "socks5 " + PROXY_IP + " " + PROXY_PORT + "\n"

    f = open(PROXYCHAINS_PATH, 'wb')
    f.write(pc_config)
    f.close()


def docker_proxy_config():
    os.system("mkdir -p " + DOCKER_SERVICE_PATH)
    os.system("rm -rf " + HTTP_PROXY_PATH)
    os.system("rm -rf " + HTTPS_PROXY_PATH)

    # http proxy
    http_proxy_config = "[Service]\n"
    http_proxy_config += 'Environment="HTTP_PROXY=http://{0}:{1}/"\n'.\
        format(PROXY_IP, PROXY_PORT)

    f = open(HTTP_PROXY_PATH, 'wb')
    f.write(http_proxy_config)
    f.close()

    # https proxy
    https_proxy_config = "[Service]\n"
    https_proxy_config += 'Environment="HTTPS_PROXY=https://{0}:{1}/"\n'. \
        format(PROXY_IP, PROXY_PORT)

    f = open(HTTPS_PROXY_PATH, 'wb')
    f.write(https_proxy_config)
    f.close()

    os.system("systemctl daemon-reload")
    os.system("systemctl restart docker")


if __name__ == '__main__':
    pc_config()
    docker_proxy_config()
