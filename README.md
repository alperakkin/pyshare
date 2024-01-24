# pyshare

## DEFINITION
This module creates link between two python applications to import python objects or download files via socket connection as a proof of concept.

Security-related constraints have not yet been addressed. Therefore, take this into consideration when using this code.

## QUICK START

### Import pyshare object both end side in the same application


```python
# Application on machine 10.0.0.10
from pyshare import PyShare

PORT = 5555
share = PyShare(PORT)

myobj = {"foo": "bar"}
share.attach("myobj", myobj)


```

On the other endpoint to collect the python object
```python
# Application on machine 10.0.0.20
from pyshare import PyShare

PORT = 5555

share = PyShare(PORT)

OTHER_MACHINE = ("10.0.0.10", PORT)

myobj = share.import_from(OTHER_MACHINE, "myobj")

print(myobj["foo"])


import pandas

dt = share.import_from(OTHER_MACHINE, "dt")


```

After running the code you will see the stdout as follows

```bash
$ bar
```

It is possible to import high level objects like pandas or numpy
Make sure that related object dependencies installed with pip

```bash
$ pip install pandas
```

```python
# Application on machine 10.0.0.20
from pyshare import PyShare
import pandas
PORT = 5555

share = PyShare(PORT)

OTHER_MACHINE = ("10.0.0.10", PORT)

dt = share.import_from(OTHER_MACHINE, "dt")

print(dt)
```

After running the code you will see the stdout as follows

```bash
$
   foo   bar
0   1     4
1   2     5
2   3     6
```

### Download a file from the other end of the network


```python
# Application on machine 10.0.0.10
from pyshare import PyShare

PORT = 5555
share = PyShare(PORT)


share.share_folder("/path/to")

```

On the other endpoint to collect the python object
```python
# Application on machine 10.0.0.20
from pyshare import PyShare

PORT = 5555

share = PyShare(PORT)

OTHER_MACHINE = ("10.0.0.10", PORT)

share.get_file(OTHER_MACHINE, "/path/to/source.png", "destination.png")


```


This will download source.png from the other end of the network and writes as detination.png