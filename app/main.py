import json
import pprint
from datetime import datetime
from wsgiref.util import request_uri

def application(env, start_resp):
    text = json.dumps({"time" : datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"), "url": request_uri(env)})    
    text1 = text.encode('utf-8')
    start_resp('200 OK', [('Content-Type', 'application/json')])
    # pprint.pprint(env)
    return [text1]
