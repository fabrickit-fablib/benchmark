# coding: utf-8

from fabkit import *  # noqa
from fablib.base import SimpleBase


class Benchmark(SimpleBase):
    def __init__(self):
        print 'init'
        self.packages = {
            'CentOS Linux 7.*': [
                'epel-release',
                'siege',
                'httpd',
                'nginx',
                'at',
                'perf',
                'sysstat',  # iostat
                'mtr',
                'traceroute',
                'strace',
                'ltrace',
                'blktrace',
                'tcpdump',
                {'name': 'nicstat', 'path': 'http://packages.psychotic.ninja/7/base/x86_64/RPMS//nicstat-1.95-3.el7.psychotic.x86_64.rpm'},  # noqa
                'iptraf-ng',
                'iotop',
                'tiptop',
                'collectl',
                'atop',
                'dstat',
                {'name': 'mysql-workbench-community', 'path': 'https://dev.mysql.com/get/Downloads/MySQLGUITools/mysql-workbench-community-6.3.9-1.el7.x86_64.rpm'},  # noqa
                'mariadb-server',
                'systemtap',
                'numactl',
                'ethtool',
                'iperf3',
                'fio',
            ],
        }

        self.services = {
            'CentOS Linux 7.*': [
                'httpd',
                'mariadb',
                'atd',
            ],
        }

    def setup(self):
        self.init()

        sudo('setenforce 0')
        Editor('/etc/selinux/config').s('SELINUX=enforcing', 'SELINUX=disable')
        Service('firewalld').stop().disable()

        self.install_packages()
        self.start_services()

        filer.template('/var/www/html/index.html')
