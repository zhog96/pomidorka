from unittest import TestCase
import testing.postgresql
import psycopg2
import json

from app import app

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
            rv = self.app.post('/api/chats/?limit=100')
            testJson = [{'chat_id': 1, 'is_group_chat': True, 'last_message': None, 'topic': 'eversome chat'}]
            self.assertTrue( compare_json_data(testJson, rv.json), str(testJson) + ' != ' + str(rv.json))
            self.assertEqual('200 OK', rv.status)
        
        with self.subTest():
            rv = self.app.post('/api/chats/?limit=1')
            testJson = [{'chat_id': 1, 'is_group_chat': True, 'last_message': None, 'topic': 'eversome chat'}]
            self.assertTrue(
                compare_json_data(testJson, rv.json), str(testJson) + ' != ' + str(rv.json))
            self.assertEqual('200 OK', rv.status)
        
        with self.subTest():
            rv = self.app.post('/api/chats/?limit=-123')
            testJson = None
            self.assertTrue(
                compare_json_data(testJson, rv.json), str(testJson) + ' != ' + str(rv.json))
            self.assertEqual('400 BAD REQUEST', rv.status)

        with self.subTest():
            rv = self.app.post('/api/chats/?limit=ewf3')
            testJson = None
            self.assertTrue(
                compare_json_data(testJson, rv.json), str(testJson) + ' != ' + str(rv.json))
            self.assertEqual('400 BAD REQUEST', rv.status)

        with self.subTest():
            rv = self.app.post('/api/chats/')
            testJson = None
            self.assertTrue(
                compare_json_data(testJson, rv.json), str(testJson) + ' != ' + str(rv.json))
            self.assertEqual('400 BAD REQUEST', rv.status)

    def test_search_user(self):
        self.clearDB()

        with self.subTest():
            rv = self.app.post('/api/user/?user_id=1')
            testJson = {'avatar': None, 'name': 'Petrovich', 'nick': 'qwerty111', 'user_id': 1}
            self.assertTrue(
                compare_json_data(testJson, rv.json), str(testJson) + ' != ' + str(rv.json))
            self.assertEqual('200 OK', rv.status)

        with self.subTest():
            rv = self.app.post('/api/user/?user_id=2')
            testJson = {'avatar': None, 'name': 'DedPihto', 'nick': 'fgh5365', 'user_id': 2}
            self.assertTrue(
                compare_json_data(testJson, rv.json), str(testJson) + ' != ' + str(rv.json))
            self.assertEqual('200 OK', rv.status)

        with self.subTest():
            rv = self.app.post('/api/user/?user_id=34')
            testJson = None
            self.assertTrue(
                compare_json_data(testJson, rv.json), str(testJson) + ' != ' + str(rv.json))
            self.assertEqual('200 OK', rv.status)

        with self.subTest():
            rv = self.app.post('/api/user/?user_id=3db')
            testJson = None
            self.assertTrue(
                compare_json_data(testJson, rv.json), str(testJson) + ' != ' + str(rv.json))
            self.assertEqual('400 BAD REQUEST', rv.status)

        with self.subTest():
            rv = self.app.post('/api/user/')
            testJson = None
            self.assertTrue(
                compare_json_data(testJson, rv.json), str(testJson) + ' != ' + str(rv.json))
            self.assertEqual('400 BAD REQUEST', rv.status)

    def test_messages(self):
        self.clearDB()

        with self.subTest():
            rv = self.app.post('/api/messages/?limit=1&chat_id=1')
            testJson = [{'added_at': '#joker', 'content': {'text': '111'}, 'message_id': 1, 'name': 'Petrovich', 'nick': 'qwerty111', 'user_id': 1}]
            self.assertTrue(
                compare_json_data(testJson, rv.json), str(testJson) + ' != ' + str(rv.json))
            self.assertEqual('200 OK', rv.status)

        with self.subTest():
            rv = self.app.post('/api/messages/?limit=10&chat_id=1')
            testJson = [{'added_at': '#joker', 'content': {'text': '111'}, 'message_id': 1, 'name': 'Petrovich', 'nick': 'qwerty111', 'user_id': 1}, {'added_at': '#joker', 'content': {'text': '222'}, 'message_id': 2, 'name': 'DedPihto', 'nick': 'fgh5365', 'user_id': 2}]
            self.assertTrue(
                compare_json_data(testJson, rv.json), str(testJson) + ' != ' + str(rv.json))
            self.assertEqual('200 OK', rv.status)

        with self.subTest():
            rv = self.app.post('/api/messages/?limit=1')
            testJson = None
            self.assertTrue(
                compare_json_data(testJson, rv.json), str(testJson) + ' != ' + str(rv.json))
            self.assertEqual('400 BAD REQUEST', rv.status)

        with self.subTest():
            rv = self.app.post('/api/messages/?chat_id=regpo&limit=123')
            testJson = None
            self.assertTrue(
                compare_json_data(testJson, rv.json), str(testJson) + ' != ' + str(rv.json))
            self.assertEqual('400 BAD REQUEST', rv.status)

    def test_create_pers_chat(self):
        self.clearDB()

        with self.subTest():
            rv = self.app.post('/api/create_pers_chat/')
            testJson = None
            self.assertTrue(
                compare_json_data(testJson, rv.json), str(testJson) + ' != ' + str(rv.json))
            self.assertEqual('400 BAD REQUEST', rv.status)

        with self.subTest():
            rv = self.app.post('/api/create_pers_chat/?topic=someTopic')
            testJson = None
            self.assertTrue(
                compare_json_data(testJson, rv.json), str(testJson) + ' != ' + str(rv.json))
            self.assertEqual('200 OK', rv.status)
            rv = self.app.post('/api/chats/?limit=100')
            testJson = [{'chat_id': 1, 'is_group_chat': True, 'last_message': None, 'topic': 'eversome chat'}, {'chat_id': 2, 'is_group_chat': False, 'last_message': None, 'topic': 'someTopic'}]
            self.assertTrue(
                compare_json_data(testJson, rv.json), str(testJson) + ' != ' + str(rv.json))
            self.assertEqual('200 OK', rv.status)

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
