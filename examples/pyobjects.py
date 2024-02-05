from pyshare import PyShare
import numpy
import pandas
PORT = 5555
OTHER_MACHINE = ('192.168.1.160', PORT)

share = PyShare(PORT)

share.attach('float_type', 1.23)
share.attach('dict_type', {'foo': 'bar'})
share.attach('int_type', 2)
share.attach('str_type', "Hello World!")
share.attach('numpy_array', numpy.array([1, 2, 3, 4, 6]))

dt = pandas.DataFrame({'foo': [1, 2, 3], 'bar': [3, 4, 5]})
share.attach('pandas', dt)
out = share.import_from(OTHER_MACHINE, 'float_type')

print('float', out)

out = share.import_from(OTHER_MACHINE, 'dict_type')

print('dict', out)

out = share.import_from(OTHER_MACHINE, 'int_type')

print('int', out)

out = share.import_from(OTHER_MACHINE, 'str_type')

print('str', out)

out = share.import_from(OTHER_MACHINE, 'numpy_array')

print('numpy', out)

out = share.import_from(OTHER_MACHINE, 'pandas')

print('pandas', out)
