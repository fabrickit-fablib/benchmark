# coding: utf-8

import copy
import json
import re
from fabkit import *  # noqa
from fablib.base import SimpleBase


class Fio(SimpleBase):
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
                'fio',
            ],
        }

        self.services = {}

    def prepare(self):
        self.init()
        self.install_packages()
        filer.mkdir('/tmp/fio')
        filer.template('/tmp/fio_job.ini')

    def bench(self):
        self.init()

        sudo('fio --output=/tmp/fio_out.json --output-format=json /tmp/fio_job.ini')
        with api.hide('stdout'):
            result = run('cat /tmp/fio_out.json')

        data = {}
        result = json.loads(result)
        global_options = result['global options']
        for job in result['jobs']:
            options = copy.deepcopy(global_options)
            options.update(job['job options'])
            rw = options['rw']
            bs = options['bs']
            iodepth = options['iodepth']
            numjobs = options.get('numjobs', 1)
            name = '{0}_{1}_qd{2}_j{3}'.format(rw, bs, iodepth, numjobs)

            data[name] = {
                'read_iops': job['read']['iops'],
                'read_latency': job['read']['clat_ns']['percentile']['99.000000'],
                'write_iops': job['write']['iops'],
                'write_latency': job['write']['clat_ns']['percentile']['99.000000'],
                'cpu_usr': job['usr_cpu'],
                'cpu_sys': job['sys_cpu'],
                'cpu_ctx': job['ctx'],
            }

        return data
