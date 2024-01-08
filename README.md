# pyshare
Sharing python objects via sockets
          ![pyshare](https://github.com/alperakkin/pyshare/assets/25936659/42e43833-4a07-4c16-89c4-11e3e55ceb1a)


## DEFINITION
This module creates link between to python applications to share simple python objects via socket connection as a proof of concept.

Security-related constraints have not yet been addressed. Therefore, take this into consideration when using this code.

## USAGE

Import pyshare object both end side in the same application

Setup yaml file for the same application on machine (Enter the appropriate ip address of your needs)
```yaml
receiver:
    5555
send_to:
    address: 10.0.0.20
    port: 5555
```

```python
# Application on machine 10.0.0.10
from pyshare import PyShare
share = PyShare()
```

Send desired python object as follows:

```python
my_object = {"foo": "bar"}
share.send_obj(my_object)
```

On the other endpoint to collect the python object
```python
# Application on machine 10.0.0.20
from pyshare import PyShare
share = PyShare()
my_obj = share.receive_obj()

print(my_obj["foo"])
```

After running the code you will see the stdout as follows

```bash
$ bar
```
