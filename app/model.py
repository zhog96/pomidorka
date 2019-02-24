from . import db
from . import cache
from flask import request, abort, jsonify,redirect, url_for, session
import json

# Here!
def list_messages_by_chat(chat_id, limit):
    rv_limit = cache.get("chats_{}_limit".format(int(chat_id)))
    rv = cache.get("chats_{}".format(int(chat_id)))
    if (rv is None) or (rv_limit is None) or (int(rv_limit) != limit):
        rv = list_messages_by_chat_nocache(chat_id, limit)
        cache.set("chats_{}_limit".format(int(chat_id)),
                  str(limit),
                  timeout = 5 * 60)
        cache.set("chats_{}".format(int(chat_id)),
                  rv,
                  timeout = 5 * 60)
    return rv

def send_message(chat_id, user_id, content):
    for i in range (0, 1000000):
        t = 2 * 2 * 2 * 2 * 2
    send_message_nocache(chat_id, user_id, content)
    cache.delete("chats_{}".format(int(chat_id)))
###

def list_messages_by_chat_nocache(chat_id, limit):
    return db.query_all("""
        SELECT user_id, nick, name,
            message_id, added_at
        FROM messages
        JOIN users USING (user_id)
        WHERE chat_id = %(chat_id)s
        ORDER BY added_at DESC
        LIMIT %(limit)s
    """, chat_id = int(chat_id), 
         limit   = int(limit))

def list_attachs(message_id, limit):
    return db.querry_all("""
        SELECT attach_id, message_id, data
        FROM attachs
        WHERE message_id = %(message_id)s
        ORDER BY attach_id DESC
        LIMIT %(limit)s
    """, message_id = int(message_id),
         limit      = int(limit))

def search_user(user_id):
    return db.query_one("""
        SELECT * 
        FROM users 
        WHERE user_id = %(user_id)s
    """, user_id = int(user_id))

def list_chats(limit):
    return db.query_all("""
        SELECT *
        FROM chats
        LIMIT %(limit)s
    """, limit   = int(limit))

def create_pers_chat(topic):
    db.execute("""
        INSERT INTO chats (is_group_chat, topic)
        VALUES (FALSE, %(topic)s);
    """, topic = topic)
    db.commit()

def send_message_nocache(chat_id, user_id, content):
    db.execute("""
        INSERT INTO messages (chat_id, user_id)
        VALUES (%(chat_id)s, %(user_id)s);
    """, chat_id = int(chat_id),
         user_id = int(user_id)
    )
    
    message_id = db.query_one("""
        SELECT message_id
        FROM messages 
        WHERE chat_id = %(chat_id)s
        ORDER BY message_id DESC
        LIMIT 1
    """, chat_id = int(chat_id))
    
    message_id = jsonify(message_id).json['message_id']

    for attach in content:
        db.execute("""
            INSERT INTO attachs (message_id, data)
            VALUES (%(message_id)s, %(data)s);
        """, message_id = int(message_id), 
             data = str(attach)
        )
    db.commit()

def read_messages(chat_id, user_id):
    db.execute("""
        UPDATE members
        SET last_read_message_id = (
            SELECT message_id
            FROM messages
            WHERE chat_id = %(chat_id)s
            ORDER BY message_id DESC
            LIMIT 1
        )
        WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s
    """, chat_id = int(chat_id), user_id = int(user_id))
    db.commit()

def member(chat_id, user_id):
    return db.query_one("""
        SELECT * FROM members
        WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s
    """, chat_id = int(chat_id), user_id = int(user_id))























    
