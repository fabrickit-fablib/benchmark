# coding: utf-8

import re
from fabkit import *  # noqa
from fablib.base import SimpleBase


class Sysbench(SimpleBase):
    def __init__(self):
        self.data_key = 'sysbench'
        self.data = {
            'mysql': {
                'user': 'sysbench',
                'password': 'sysbench',
                'database': 'sysbench',
            },
            'oltp_option': {
                'range_size': 100,
                'table_size': 10000000,
                'tables': 2,
                'threads': 1,
                'events': 0,
                'time': 60,
            },
        }

        self.packages = {
            'CentOS Linux 7.*': [
                'epel-release',
                'sysbench',
                'mariadb-server',
            ],
        }

        self.services = {
            'CentOS Linux 7.*': [
                'mariadb',
            ]
        }

    def prepare(self):
        data = self.init()

        sudo('setenforce 0')
        Editor('/etc/selinux/config').s('SELINUX=enforcing', 'SELINUX=disable')
        Service('firewalld').stop().disable()

        self.install_packages()
        self.start_services()
        self.sql('CREATE DATABASE IF NOT EXISTS {0};'.format(data['mysql']['database']))
        self.sql("GRANT ALL ON {0}.* TO {1}@'localhost' IDENTIFIED BY '{2}'".format(
            data['mysql']['database'], data['mysql']['user'], data['mysql']['password']
        ))

    def sql(self, query):
        sudo('mysql -uroot -e"{0}"'.format(query))

    def bench_memory(self):
        self.init()
        seq_write_1k = self.bench_memory_cmd(bs='1K', oper='write', mode='seq')
        seq_read_1k = self.bench_memory_cmd(bs='1K', oper='read', mode='seq')
        rnd_write_1k = self.bench_memory_cmd(bs='1K', oper='write', mode='rnd')
        rnd_read_1k = self.bench_memory_cmd(bs='1K', oper='read', mode='rnd')

        return {
            'seq_write_1k': seq_write_1k,
            'seq_read_1k': seq_read_1k,
            'rnd_write_1k': rnd_write_1k,
            'rnd_read_1k': rnd_read_1k,
        }

    def bench_memory_cmd(self, bs='1K', total_size='100G', oper='write', mode='seq'):
        result = run(
            'sysbench --threads=1 memory run --memory-block-size={bs} --memory-total-size={total_size}'
            ' --memory-oper={oper} --memory-access-mode={mode}'.format(
                bs=bs, total_size=total_size, oper=oper, mode=mode))

        re_transferred = re.compile('transferred \(([0-9\.]+) MiB/sec')
        match_transferred = re_transferred.search(result)
        transferred = match_transferred.group(1)

        return transferred

    def bench_oltp(self):
        self.bench_oltp_cmd('cleanup')
        self.bench_oltp_cmd('prepare')
        self.bench_oltp_cmd('run')  # for warming up
        result = self.bench_oltp_cmd('run')

        re_transactions = re.compile('transactions: +[0-9]+ +\(([0-9\.]+) .*')
        match_transactions = re_transactions.search(result)
        transactions = match_transactions.group(1)

        re_queries = re.compile('queries: +[0-9]+ +\(([0-9\.]+) .*')
        match_queries = re_queries.search(result)
        queries = match_queries.group(1)

        return {
            'transactions_per_sec': transactions,
            'queries_per_sec': queries,
        }

    def bench_oltp_cmd(self, action):
        data = self.init()

        result = run(
            'sysbench --db-driver=mysql --mysql-user={mysql[user]} --mysql-password={mysql[password]} '
            ' --mysql-socket=/var/lib/mysql/mysql.sock --mysql-db={mysql[database]} '
            ' --range_size={option[range_size]} --table_size={option[table_size]} --tables={option[tables]} '
            ' --threads={option[threads]} --events={option[events]} --time={option[time]} '
            ' /usr/share/sysbench/oltp_read_write.lua {action}'.format(
                mysql=data['mysql'],
                option=data['oltp_option'],
                action=action,
            ))

        return result
