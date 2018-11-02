from flask import request, jsonify, abort
from . import model
from . import app

def _tryNone(param):
    param = request.args.get(param)
    if param is None:
        abort(400)
    return param

def tryString(param):
    return _tryNone(param)

def tryInt(param):
    param = _tryNone(param)
    try:
        param = int(param)
    except ValueError:
        abort(400)
    return param

def tryIntMoreThen(param, moreThen):
    param = tryInt(param)
    if param <= moreThen:
        abort(400)
    return param

@app.route('/api/messages/', methods = ['POST'])
def messages():
    chat_id = tryIntMoreThen('chat_id', 0)
    limit = tryIntMoreThen('limit', 0)
    messages = model.list_messages_by_chat(chat_id, limit)
    return jsonify(messages)

@app.route('/api/user/', methods = ['POST'])
def user():
    user_id = tryIntMoreThen('user_id', 0)
    user = model.search_user(user_id)
    return jsonify(user)
    
@app.route('/api/chats/', methods = ['POST'])
def chats():
    limit = tryIntMoreThen('limit', 0)
    chats = model.list_chats(limit)
    return jsonify(chats)

@app.route('/api/create_pers_chat/', methods = ['POST'])
def create_pers_chat():
    topic = tryString('topic')
    e = model.create_pers_chat(topic)
    return jsonify(e)

