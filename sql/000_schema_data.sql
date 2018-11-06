INSERT INTO users (nick, name)
VALUES ('qwerty111', 'Petrovich'),
       ('fgh5365', 'DedPihto');

INSERT INTO chats (is_group_chat, topic)
VALUES (TRUE, 'eversome chat');

INSERT INTO messages (chat_id, user_id, content)
VALUES (1, 1, '{"text" : "111"}'),
       (1, 2, '{"text" : "222"}');

INSERT INTO  members (user_id, chat_id, last_read_message_id)
VALUES (1, 1, NULL),
       (2, 1, NULL);
