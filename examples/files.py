from pyshare import PyShare

PORT = 5555
OTHER_MACHINE = ('192.168.1.129', PORT)

share = PyShare(PORT)

share.share_folder("/path/to")


share.get_file(OTHER_MACHINE,
               "/path/to/source.png", "destination.png")
