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
Done.
Disconnecting from 192.168.122.101... done.
Name          Stmts   Miss  Cover   Missing
-------------------------------------------
__init__.py       7      0   100%
__________ summary ________________________
  py27: commands succeeded
  congratulations :)
```


## License
This is licensed under the MIT. See the [LICENSE](./LICENSE) file for details.
