# benchmark


## Overview
This is benchmark of fablib.


## Run benchmark by test-repo
Follow these steps.
```
$ fab test:l=benchmark,p='bootstrap|setup'
...
Done.
Disconnecting from 192.168.122.101... done.

$ ssh fabric@192.168.122.101
Warning: Permanently added '192.168.122.101' (ECDSA) to the list of known hosts.
fabric@192.168.122.101's password:
Last login: Sat Mar 11 06:21:04 2017 from gateway
[fabric@benchmark-1-hostname ~]$ hostname
benchmark-1-hostname
```


## Testing Guidelines
This library can be tested with tox.
Follow these steps.
```
$ tox
...
...
--------------------------------------------------------------------------
sysbench_memory
--------------------------------------------------------------------------
host                    rnd_read_1k rnd_write_1k seq_read_1k seq_write_1k
benchmark-1.example.com 1845.59     1850.77      4941.86     4202.29
--------------------------------------------------------------------------
-------------------------------------------------------------
sysbench_oltp
-------------------------------------------------------------
host                    queries_per_sec transactions_per_sec
benchmark-1.example.com 3694.24         184.71
-------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------
fio
----------------------------------------------------------------------------------------------------------------------------
host                    job                   cpu_ctx cpu_sys   cpu_usr  read_iops   read_latency write_iops  write_latency
benchmark-1.example.com randread_4k_qd1_j1    124173  17.776667 0.786667 2069.432176 700416       0.0         0
benchmark-1.example.com randread_4k_qd32_j1   133938  15.544447 4.530534 2232.438017 29491200     0.0         0
benchmark-1.example.com randread_4k_qd32_j8   1253    0.244682  0.019974 262.970422  177209344    0.0         0
benchmark-1.example.com randread_4k_qd8_j1    127628  14.370948 4.644768 2127.791481 7897088      0.0         0
benchmark-1.example.com randread_512_qd1_j1   126964  18.043333 0.733333 2115.931401 675840       0.0         0
benchmark-1.example.com randread_512k_qd1_j1  32772   10.086101 0.350367 610.67109   2113536      0.0         0
benchmark-1.example.com randwrite_4k_qd1_j1   195730  25.145    0.793333 0.0         0            3261.995633 765952
benchmark-1.example.com randwrite_4k_qd32_j1  217863  19.838691 8.971988 0.0         0            3634.044326 18743296
benchmark-1.example.com randwrite_4k_qd32_j8  1578    0.251579  0.096633 0.0         0            396.121422  173015040
benchmark-1.example.com randwrite_4k_qd8_j1   203217  19.771008 7.149762 0.0         0            3389.963835 5734400
benchmark-1.example.com randwrite_512_qd1_j1  201754  25.95     0.828333 0.0         0            3362.460626 724992
benchmark-1.example.com randwrite_512k_qd1_j1 21499   7.38321   1.079982 0.0         0            358.238059  7831552
benchmark-1.example.com read_1m_qd1_j1        16394   6.557417  0.243761 395.414505  3588096      0.0         0
benchmark-1.example.com write_1m_qd1_j1       16388   7.256253  0.943239 0.0         0            304.20736   19267584
----------------------------------------------------------------------------------------------------------------------------
```


## License
This is licensed under the MIT. See the [LICENSE](./LICENSE) file for details.
