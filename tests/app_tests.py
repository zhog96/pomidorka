from flask import request, jsonify, abort, Response
from unittest import TestCase
import testing.postgresql
import psycopg2
import json
from flask_jsonrpc.proxy import ServiceProxy

from app import app

server = ServiceProxy('http://pomidorka.com:5000/api/')

class AppTest(TestCase):
    def runScript(self, filename, connection):
        file = open(filename, 'r')
        sql = s = " ".join(file.readlines())
        cursor = connection.cursor()
        cursor.execute(sql) 
        connection.commit() 
        file.close()  

    def clearDB(self):
        conn = psycopg2.connect(**self.postgresql.dsn())
        self.runScript('tests/sql/000_schema_del.sql', conn)
        self.runScript('tests/sql/000_schema.sql', conn)
        self.runScript('tests/sql/000_schema_data.sql', conn)
    
    def setUp(self):
        name = 'testdb'
        port = '5678'
        path = '/tmp/my_test_db'
        password = 'qwerty'
        self.postgresql = testing.postgresql.Postgresql(name=name, port=int(port), base_dir=path, password=password)

        conn = psycopg2.connect(**self.postgresql.dsn())

        self.runScript('tests/sql/000_schema.sql', conn)
        self.runScript('tests/sql/000_schema_data.sql', conn)

        self.app = app.test_client()

    def test_chats(self):
        self.clearDB()

        with self.subTest():
            rv = server.chats(limit = 100)
            testJson = {'id': '#joker', 'jsonrpc': '2.0', 'result': [{'chat_id': 1, 'is_group_chat': True, 'last_message': None, 'topic': 'eversome chat'}]}
            self.assertTrue(compare_json_data(testJson, rv), str(testJson) + ' != ' + str(rv))
        
        with self.subTest():
            rv = server.chats(limit = -123)
            testJson = {'error': {'code': -32602, 'data': None, 'message': 'InvalidParamsError: Invalid params.', 'name': 'InvalidParamsError'}, 'id': '#joker', 'jsonrpc': '2.0'}
            self.assertTrue(compare_json_data(testJson, rv), str(testJson) + ' != ' + str(rv))

        with self.subTest():
            rv = server.chats()
            testJson = {'error': {'code': 500, 'data': None, 'message': "OtherError: chats() missing 1 required positional argument: 'limit'", 'name': 'OtherError'}, 'id': '#joker', 'jsonrpc': '2.0'}
            self.assertTrue(compare_json_data(testJson, rv), str(testJson) + ' != ' + str(rv))

    def test_search_user(self):
        self.clearDB()
        
        with self.subTest():
            rv = server.user(user_id = 1)
            testJson = {'id': '#joker', 'jsonrpc': '2.0', 
                'result': {'avatar': None, 'name': 'Petrovich', 'nick': 'qwerty111', 'user_id': 1}}
            self.assertTrue(compare_json_data(testJson, rv), str(testJson) + ' != ' + str(rv))

        with self.subTest():
            rv = server.user(user_id = 2)
            testJson ={'id': '#joker', 'jsonrpc': '2.0', 'result': {'avatar': None, 'name': 'DedPihto', 'nick': 'fgh5365', 'user_id': 2}}
            self.assertTrue(compare_json_data(testJson, rv), str(testJson) + ' != ' + str(rv))

        with self.subTest():
            rv = server.user(user_id = 34)
            testJson = {'id': '#joker', 'jsonrpc': '2.0', 'result': None}
            self.assertTrue(compare_json_data(testJson, rv), str(testJson) + ' != ' + str(rv))

    def test_messages(self):
        self.clearDB()

        with self.subTest():
            rv = server.messages(chat_id = 1, limit = 100)
            testJson = {'id': '#joker', 'jsonrpc': '2.0', 'result': [{'added_at': '#joker', 'content': {'text': '111'}, 'message_id': 1, 'name': 'Petrovich', 'nick': 'qwerty111', 'user_id': 1}, {'added_at': '#joker', 'content': {'text': '222'}, 'message_id': 2, 'name': 'DedPihto', 'nick': 'fgh5365', 'user_id': 2}]}
            self.assertTrue(compare_json_data(testJson, rv), str(testJson) + ' != ' + str(rv))

        with self.subTest():
            rv = server.messages(chat_id = 1, limit = 1)
            testJson = {'id': '#joker', 'jsonrpc': '2.0', 'result': [{'added_at': '#joker', 'content': {'text': '111'}, 'message_id': 1, 'name': 'Petrovich', 'nick': 'qwerty111', 'user_id': 1}]}
            self.assertTrue(compare_json_data(testJson, rv), str(testJson) + ' != ' + str(rv))

        with self.subTest():
            rv = server.messages(chat_id = 0, limit = 1)
            testJson = {'error': {'code': -32602, 'data': None, 'message': 'InvalidParamsError: Invalid params.', 'name': 'InvalidParamsError'}, 'id': '#joker', 'jsonrpc': '2.0'}
            self.assertTrue(compare_json_data(testJson, rv), str(testJson) + ' != ' + str(rv))

    def test_create_pers_chat(self):
        self.clearDB()
        
        with self.subTest():
            rv = server.create_pers_chat()
            testJson = {'error': {'code': 500, 'data': None, 'message': "OtherError: create_pers_chat() missing 1 required positional argument: 'topic'", 'name': 'OtherError'}, 'id': '#joker', 'jsonrpc': '2.0'}
            self.assertTrue(compare_json_data(testJson, rv), str(testJson) + ' != ' + str(rv))

        with self.subTest():
            rv = server.create_pers_chat(topic = 'asdasdasd')
            testJson = {'id': '#joker', 'jsonrpc': '2.0', 'result': None}
            self.assertTrue(compare_json_data(testJson, rv), str(testJson) + ' != ' + str(rv))
            
            rv = server.chats(limit = 100)
            testJson = {'id': '#joker', 'jsonrpc': '2.0', 'result': [{'chat_id': 1, 'is_group_chat': True, 'last_message': None, 'topic': 'eversome chat'}, {'chat_id': 2, 'is_group_chat': False, 'last_message': None, 'topic': 'asdasdasd'}]}
            self.assertTrue(compare_json_data(testJson, rv), str(testJson) + ' != ' + str(rv))

    def test_send_message(self):
        self.clearDB()
        
        with self.subTest():
            rv = server.send_message(chat_id = 1, user_id = 6, content = json.dumps({'text' : 'Hello'}))
            testJson = {'error': {'code': 500, 'data': None, 'message': 'OtherError: insert or update on table "messages" violates foreign key constraint "messages_user_id_fkey"\nDETAIL:  Key (user_id)=(6) is not present in table "users".\n', 'name': 'OtherError'}, 'id': '#joker', 'jsonrpc': '2.0'}
            self.assertTrue(compare_json_data(testJson, rv), str(testJson) + ' != ' + str(rv))

        with self.subTest():
            rv = server.send_message(chat_id = 1, user_id = 1, content = json.dumps({'text' : 'Hello'}))
            testJson = {'id': '#joker', 'jsonrpc': '2.0', 'result': None}
            self.assertTrue(compare_json_data(testJson, rv), str(testJson) + ' != ' + str(rv))

            rv = server.messages(chat_id = 1, limit = 100)
            testJson = {'id': '#joker', 'jsonrpc': '2.0', 'result': [{'added_at': '#joker', 'content': {'text': 'Hello'}, 'message_id': 4, 'name': 'Petrovich', 'nick': 'qwerty111', 'user_id': 1}, {'added_at': '#joker', 'content': {'text': '111'}, 'message_id': 1, 'name': 'Petrovich', 'nick': 'qwerty111', 'user_id': 1}, {'added_at': '#joker', 'content': {'text': '222'}, 'message_id': 2, 'name': 'DedPihto', 'nick': 'fgh5365', 'user_id': 2}]}
            self.assertTrue(compare_json_data(testJson, rv), str(testJson) + ' != ' + str(rv))

    def tearDown(self):
        conn = psycopg2.connect(**self.postgresql.dsn())
        cursor = conn.cursor()
        self.runScript('tests/sql/000_schema_del.sql', conn)
        self.postgresql.stop()

def compare_json_data(source_data_a,source_data_b):

	def compare(data_a,data_b):
		# type: list
		if (type(data_a) is list):
			# is [data_b] a list and of same length as [data_a]?
			if (
				(type(data_b) != list) or
				(len(data_a) != len(data_b))
			):
				return False

			# iterate over list items
			for list_index,list_item in enumerate(data_a):
				# compare [data_a] list item against [data_b] at index
				if (not compare(list_item,data_b[list_index])):
					return False

			# list identical
			return True

		# type: dictionary
		if (type(data_a) is dict):
			# is [data_b] a dictionary?
			if (type(data_b) != dict):
				return False

			# iterate over dictionary keys
			for dict_key,dict_value in data_a.items():
				# key exists in [data_b] dictionary, and same value?
				if (
					(dict_key not in data_b) or
					(not compare(dict_value,data_b[dict_key]))
				):
					return False

			# dictionary identical
			return True

		# simple value - compare both value and type for equality
		return (
			((data_a == data_b) and
			(type(data_a) is type(data_b))) or
            ((str(data_a) == '#joker') or (str(data_b) == '#joker'))
		)

	# compare a to b, then b to a
	return (
		compare(source_data_a,source_data_b) and
		compare(source_data_b,source_data_a)
	)

if __name__ == "__main__":
    unittest.main()
