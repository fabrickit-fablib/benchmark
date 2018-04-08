# coding: utf-8

from fabkit import task, util
from fablib.benchmark import Sysbench, Fio


@task
def fio():
    bench = Fio()
    bench.prepare()
    data = bench.bench()
    return {
        'status': 0,
        'data_map': {
            'fio': {
                'type': 'multi-table',
                'data': data,
            },
        }
    }


@task
def sysbench():
    bench = Sysbench()
    bench.prepare()
    sysbench_memory = bench.bench_memory()
    sysbench_oltp = bench.bench_oltp()

    return {
        'status': 0,
        'data_map': {
            'sysbench_memory': {
                'type': 'table',
                'data': sysbench_memory,
            },
            'sysbench_oltp': {
                'type': 'table',
                'data': sysbench_oltp,
            }
        }
    }


@task
def report():
    sysbench_memory = util.get_datamap('sysbench_memory')
    sysbench_oltp = util.get_datamap('sysbench_oltp')
    # If you needed, send datamap to your reporting systems
    print sysbench_memory
    print sysbench_oltp

    util.print_datamap('sysbench_memory')
    util.print_datamap('sysbench_oltp')
    util.print_datamap('fio')
