from flask import request, jsonify, abort, Response
from . import model
from . import app
from . import jsonrpc
from flask_jsonrpc.exceptions import *


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
