from pyshare import PyShare
PORT = 5555
OTHER_MACHINE = ('192.168.1.3', PORT)

share = PyShare(PORT)

share.attach('float_type', 1.23)
share.attach('dict_type', {'foo': 'bar'})
share.attach('int_type', 2)
share.attach('str_type', "Hello World!")
out = share.import_from(OTHER_MACHINE, 'float_type')

print('float', out)

out = share.import_from(OTHER_MACHINE, 'dict_type')

print('dict', out)

out = share.import_from(OTHER_MACHINE, 'int_type')

print('int', out)

out = share.import_from(OTHER_MACHINE, 'str_type')

print('str', out)
