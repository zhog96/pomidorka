from cent import Client
import json

from . import app
from . import jsonrpc

"""class Centrifugo:
    def __init__(self):
        self.url = 'http://localhost:8000'
        file = open('../centrifugo/config.json', 'r')
        config = json.load(file)
        self.api_key = config['api_key']
        file.close()
        self.client = Client(self.url, api_key=self.api_key, timeout=1)

    def run(self):
        channel = 'public:chat'
        data = {'input': 'test'}
        self.client.publish(channel, data)

centrifugo = Centrifugo()
centrifugo.run()"""
