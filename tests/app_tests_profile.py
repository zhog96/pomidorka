from flask import request, jsonify, Response
from unittest import TestCase
import testing.postgresql
import psycopg2
import json
from flask_jsonrpc.proxy import ServiceProxy
import subprocess
import time

from app import app

server = ServiceProxy('http://pomidorka.com:5000/api/')
        
class AppTest(TestCase):    
    class DB:
        def __init__(self, config):
            self.postgresql = testing.postgresql.Postgresql(
                    name     = config['db']['name'], 
                    port     = int(config['db']['port']), 
                    base_dir = config['db']['path'], 
                    password = config['db']['password'])
            conn = psycopg2.connect(**self.postgresql.dsn())

            self.sql_set_up = config['db']['sql_set_up']
            self.sql_fill = config['db']['sql_fill']
            self.sql_del = config['db']['sql_del']

            #self.runScript(self.sql_del, conn)
            self.runScript(self.sql_set_up, conn)
            self.runScript(self.sql_fill, conn)
            self.app = app.test_client()
    
        def refresh(self):
            conn = psycopg2.connect(**self.postgresql.dsn())
            self.runScript(self.sql_del, conn)
            self.runScript(self.sql_set_up, conn)
            self.runScript(self.sql_fill, conn)

        def delete(self):
            conn = psycopg2.connect(**self.postgresql.dsn())
            cursor = conn.cursor()
            self.runScript(self.sql_del, conn)
            self.postgresql.stop()

        def runScript(self, filename, connection):
            file = open(filename, 'r')
            sql = s = " ".join(file.readlines())
            cursor = connection.cursor()
            cursor.execute(sql) 
            connection.commit() 
            file.close() 

# Here! 
    def test_profile(self):
        self.db.refresh()

        with self.subTest():
            result = server.messages(chat_id = 1, limit = 100)
            test_json = {'id': '#joker', 'jsonrpc': '2.0', 'result': [      {'added_at': '#joker',
 'message_id': 5,  'name': 'Petrovich', 'nick': 'qwerty111', 'user_id': 1}, {'added_at': '#joker',
 'message_id': 4,  'name': 'Petrovich', 'nick': 'qwerty111', 'user_id': 1}, {'added_at': '#joker',
 'message_id': 3,  'name': 'Petrovich', 'nick': 'qwerty111', 'user_id': 1}, {'added_at': '#joker',
 'message_id': 2,  'name': 'Petrovich', 'nick': 'qwerty111', 'user_id': 1}, {'added_at': '#joker',
 'message_id': 1,  'name': 'Petrovich', 'nick': 'qwerty111', 'user_id': 1}, {'added_at': '#joker',
 'message_id': 10, 'name': 'Fridrih',   'nick': 'kokoko123', 'user_id': 2}, {'added_at': '#joker',
 'message_id': 9,  'name': 'Fridrih',   'nick': 'kokoko123', 'user_id': 2}, {'added_at': '#joker',
 'message_id': 8,  'name': 'Fridrih',   'nick': 'kokoko123', 'user_id': 2}, {'added_at': '#joker',
 'message_id': 7,  'name': 'Fridrih',   'nick': 'kokoko123', 'user_id': 2}, {'added_at': '#joker',
 'message_id': 6,  'name': 'Fridrih',   'nick': 'kokoko123', 'user_id': 2}]}
            self.assertTrue(compare_json_data(test_json, result), str(test_json) + ' != ' + str(result))

        with self.subTest():
            server.send_message(1, 1, ['Balalayka'])
            result = server.messages(chat_id = 1, limit = 100)
            test_json = {'id': '#joker', 'jsonrpc': '2.0', 'result': [      {'added_at': '#joker',
 'message_id': 51, 'name': 'Petrovich', 'nick': 'qwerty111', 'user_id': 1}, {'added_at': '#joker',
 'message_id': 5,  'name': 'Petrovich', 'nick': 'qwerty111', 'user_id': 1}, {'added_at': '#joker',
 'message_id': 4,  'name': 'Petrovich', 'nick': 'qwerty111', 'user_id': 1}, {'added_at': '#joker',
 'message_id': 3,  'name': 'Petrovich', 'nick': 'qwerty111', 'user_id': 1}, {'added_at': '#joker',
 'message_id': 2,  'name': 'Petrovich', 'nick': 'qwerty111', 'user_id': 1}, {'added_at': '#joker',
 'message_id': 1,  'name': 'Petrovich', 'nick': 'qwerty111', 'user_id': 1}, {'added_at': '#joker',
 'message_id': 10, 'name': 'Fridrih',   'nick': 'kokoko123', 'user_id': 2}, {'added_at': '#joker',
 'message_id': 9,  'name': 'Fridrih',   'nick': 'kokoko123', 'user_id': 2}, {'added_at': '#joker',
 'message_id': 8,  'name': 'Fridrih',   'nick': 'kokoko123', 'user_id': 2}, {'added_at': '#joker',
 'message_id': 7,  'name': 'Fridrih',   'nick': 'kokoko123', 'user_id': 2}, {'added_at': '#joker',
 'message_id': 6,  'name': 'Fridrih',   'nick': 'kokoko123', 'user_id': 2}]}
            self.assertTrue(compare_json_data(test_json, result), str(test_json) + ' != ' + str(result))
           
    def setUp(self):
        file = open('tests/config.json', 'r')
        
        db_config = json.load(file)
        self.db = AppTest.DB(config = db_config)
        file.close()

        file = open('app/config.json', 'r')
        self.saved_config = file.read()
        file.close()

        file = open('app/config.json', 'w')
        json.dump(db_config, file)
        file.close()
             
    def tearDown(self):
        self.db.delete();
        file = open('app/config.json', 'w')
        file.write(self.saved_config)
        file.close()

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
