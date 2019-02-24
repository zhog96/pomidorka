from flask import request, abort, jsonify,redirect, url_for, session
from . import model
from . import app
from . import vk
from . import jsonrpc
from . import oauth, jsonrpc
import json
from cent import Client
from flask_jsonrpc.exceptions import *
from flask import url_for, render_template

def tryNone(param):
    if param is None:
        raise InvalidParamsError()
    return param

def tryString(param):
    return tryNone(param)

def tryInt(param):
    param = tryNone(param)
    try:
        param = int(param)
    except ValueError:
        raise InvalidParamsError()
    return param

def tryIntMoreThen(param, moreThen):
    param = tryInt(param)
    if param <= moreThen:
        raise InvalidParamsError()
    return param

@jsonrpc.method('messages')
def messages(chat_id, limit):
    chat_id = tryIntMoreThen(chat_id, 0)
    limit = tryIntMoreThen(limit, 0)
    messages = model.list_messages_by_chat(chat_id, limit)
    return jsonify(messages).json

@jsonrpc.method('user')
def user(user_id):
    user_id = tryIntMoreThen(user_id, 0)
    user = model.search_user(user_id)
    return jsonify(user).json
    
@jsonrpc.method('chats')
def chats(limit):
    limit = tryIntMoreThen(limit, 0)
    chats = model.list_chats(limit)
    return jsonify(chats).json

@jsonrpc.method('attachs')
def attachs(message_id, limit):
    limit = tryIntMoreThen(limit, 0)
    message_id = tryIntMoreThen(message_id, 0)
    attachs = model.list_chats(message_id, limit)
    return jsonify(attachs).json

@jsonrpc.method('create_pers_chat')
def create_pers_chat(topic):
    topic = tryString(topic)
    e = model.create_pers_chat(topic)
    return jsonify(e).json

@jsonrpc.method('read_messages')
def read_messages(chat_id, user_id):
    chat_id = tryIntMoreThen(chat_id, 0)
    user_id = tryIntMoreThen(user_id, 0)
    return jsonify(model.read_messages(chat_id, user_id)).json

@jsonrpc.method('member')
def member(chat_id, user_id):
    chat_id = tryIntMoreThen(chat_id, 0)
    user_id = tryIntMoreThen(user_id, 0)
    return jsonify(model.member(chat_id, user_id)).json

@jsonrpc.method('send_message')
def send_message(chat_id, user_id, content):
    chat_id = tryIntMoreThen(chat_id, 0)
    user_id = tryIntMoreThen(user_id, 0)
    content = tryNone(content)
    e = model.send_message(chat_id, user_id, content)
    return jsonify(e).json








@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return vk.authorize(callback=url_for('vk_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/login/authorized')
@vk.authorized_handler
def vk_authorized(resp):
    print( "=====", resp )
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    access_token = resp['access_token']
    email = resp.get('email')
    session['oauth_token'] = (resp['access_token'], '')
    return "Email: {}".format( email )

@vk.tokengetter
def get_vk_oauth_token():
    return session.get('oauth_token')







class Centrifugo:
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

    def send(self, chat_id, user_id, msg):
        channel = 'public:chat'
        data = {
            'chat_id': chat_id,
            'user_id': user_id,
            'msg': msg
        }
        self.client.publish(channel, data)

centrifugo = Centrifugo()

@jsonrpc.method('post')
def post(chat_id, user_id, msg):
    #import ipdb
    #ipdb.set_trace()
    centrifugo.send(chat_id, user_id, msg)
    #send_message(chat_id, user_id, msg)

#curl -i -X POST        -H "Content-Type: application/json; indent=4"        -d '{ "jsonrpc": "2.0", "method": "post", "params": {"chat_id":1, "user_id":1, "msg": "123"}, "id": "1"}' http://pomidorka.com:5000/api/

    






