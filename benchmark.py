# coding: utf-8

from fabkit import *  # noqa
from fablib.base import SimpleBase


class Benchmark(SimpleBase):
    def __init__(self):
        print 'init'
        self.packages = {
            'CentOS Linux 7.*': [
                'epel-release',
                'wget',
                'python-devel',
                'siege',
                'httpd',
                'haproxy',
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
                'nginx',
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

    def sysbench_oltp(self):
        data = self.init()

        if data['hosts'][0] == env.host:
            self.sql('CREATE DATABASE IF NOT EXISTS sysbench;')
            self.sql("GRANT ALL ON sysbench.* TO sysbench@'localhost' IDENTIFIED BY 'sysbench'")

            run('sysbench --db-driver=mysql --mysql-user=sysbench --mysql-password=sysbench '
                ' --mysql-socket=/var/lib/mysql/mysql.sock --mysql-db=sysbench --range_size=100 '
                ' --table_size=10000 --tables=2 --threads=1 --events=0 --time=60 '
                ' /usr/share/sysbench/oltp_read_write.lua cleanup')

            run('sysbench --db-driver=mysql --mysql-user=sysbench --mysql-password=sysbench '
                ' --mysql-socket=/var/lib/mysql/mysql.sock --mysql-db=sysbench --range_size=100 '
                ' --table_size=10000 --tables=2 --threads=1 --events=0 --time=60 '
                ' /usr/share/sysbench/oltp_read_write.lua prepare')

            # warming up
            run('sysbench --db-driver=mysql --mysql-user=sysbench --mysql-password=sysbench '
                ' --mysql-socket=/var/lib/mysql/mysql.sock --mysql-db=sysbench --range_size=100 '
                ' --table_size=10000 --tables=2 --threads=1 --events=0 --time=60 '
                ' /usr/share/sysbench/oltp_read_write.lua run')

            result = run(
                'sysbench --db-driver=mysql --mysql-user=sysbench --mysql-password=sysbench '
                ' --mysql-socket=/var/lib/mysql/mysql.sock --mysql-db=sysbench --range_size=100 '
                ' --table_size=10000 --tables=2 --threads=1 --events=0 --time=60 '
                ' /usr/share/sysbench/oltp_read_write.lua run')

            run('sysbench --db-driver=mysql --mysql-user=sysbench --mysql-password=sysbench '
                ' --mysql-socket=/var/lib/mysql/mysql.sock --mysql-db=sysbench --range_size=100 '
                ' --table_size=10000 --tables=2 --threads=1 --events=0 --time=60 '
                ' /usr/share/sysbench/oltp_read_write.lua cleanup')

            print result
