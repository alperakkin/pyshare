# pyshare

## DEFINITION
This module creates link between to python applications to share simple python objects via socket connection as a proof of concept.

Security-related constraints have not yet been addressed. Therefore, take this into consideration when using this code.

## QUICK START

Import pyshare object both end side in the same application


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

```

After running the code you will see the stdout as follows

```bash
$ bar
```
