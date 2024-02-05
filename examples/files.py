from pyshare import PyShare

PORT = 5555
IP = '10.0.0.10'

OTHER_MACHINE = (IP, PORT)

share = PyShare(PORT)

share.share_folder("/path/to")


share.get_file(OTHER_MACHINE,
               "/path/to/source.png", "destination.png")
