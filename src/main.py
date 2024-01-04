from libs.utils import load_config, is_server
from libs.server import ShareServer
from libs.client import ShareClient
if __name__ == '__main__':

    config = load_config('config.yaml')

    if is_server(config['server']['address']):
        server = ShareServer(config)
    else:
        client = ShareClient(config)
        client.connect()
        client.send_obj({'foo': 'bar'})




