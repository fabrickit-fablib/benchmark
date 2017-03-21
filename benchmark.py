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
                'at',
                'perf',
            ],
        }

        self.services = {
            'CentOS Linux 7.*': [
                'httpd',
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
