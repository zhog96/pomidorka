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
        CHECK (length(topic) < 128)
);

CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,
    chat_id INTEGER NOT NULL
        REFERENCES chats(chat_id),
    user_id INTEGER NOT NULL
        REFERENCES users(user_id),
    added_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE members (
    member_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL
        REFERENCES users(user_id),
    chat_id INTEGER NOT NULL
        REFERENCES chats(chat_id),
    last_read_message_id INTEGER
        REFERENCES messages(message_id)
);

CREATE TABLE attachs (
    attach_id SERIAL PRIMARY KEY,
    message_id INTEGER NOT NULL
        REFERENCES messages(message_id),
    data TEXT NOT NULL
);



