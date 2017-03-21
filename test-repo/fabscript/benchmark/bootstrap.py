# coding: utf-8

from fabkit import task
from fablib.benchmark import Benchmark

benchmark = Benchmark()


@task
def setup():
    benchmark.setup()
