from . import db

def list_messages_by_chat(chat_id, limit):
    return db.query_all("""
        SELECT user_id, nick, name,
            message_id, content, added_at
        FROM messages
        JOIN users USING (user_id)
        WHERE chat_id = %(chat_id)s
        ORDER BY added_at DESC
        LIMIT %(limit)s
    """, chat_id = int(chat_id), 
         limit   = int(limit))

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
    db._commit_db()

def send_message(chat_id, user_id, content):
    db.execute("""
        INSERT INTO messages (chat_id, user_id, content)
        VALUES (%(chat_id)s, %(user_id)s, %(content)s);
    """, chat_id = int(chat_id),
         user_id = int(user_id),
         content = content)
    db._commit_db()























    
