CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    nick TEXT NOT NULL UNIQUE
        CHECK (length(nick) < 32),
    name TEXT NOT NULL
        CHECK (length(name) < 32),
    avatar TEXT
);

CREATE TABLE chats (
    chat_id SERIAL PRIMARY KEY,
    is_group_chat BOOL NOT NULL,
    topic TEXT NOT NULL
        CHECK (length(topic) < 128),
);

CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,
    chat_id INTEGER NOT NULL
        REFERENCES chats(chat_id),
    user_id INTEGER NOT NULL
        REFERENCES users(user_id),
    content JSON NOT NULL,
    added_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE members (
    user_id INTEGER NOT NULL
        REFERENCES users(user_id),
    chat_id INTEGER NOT NULL
        REFERENCES chats(chat_id),
    new_messages JSON NOT NULL,
    last_read_message_id INTEGER NOT NULL
        REFERENCES messages(message_id)
);



