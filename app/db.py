import psycopg2
import psycopg2.extras
import flask
import json
from . import app
from . import jsonrpc

def get_connection():
    if not hasattr(app, 'db_config'):
        file = open('app/config.json')
        app.db_config = json.load(file)
    if not hasattr(flask.g, 'dbconn'):
        flask.g.dbconn = psycopg2.connect(
            database = app.db_config['db']['name'],        
            host     = app.db_config['db']['host'],
            user     = app.db_config['db']['user'],
            port     = app.db_config['db']['port'],
            password = app.db_config['db']['password'])
    return flask.g.dbconn

def get_cursor():
    return get_connection().cursor(
        cursor_factory = psycopg2.extras.DictCursor)

def query_one(sql, **params):
    with get_cursor() as cur:
        cur.execute(sql, params)
        res = cur.fetchone();
        if res is None:
            return
        return dict(res)

def query_all(sql, **params):
    with get_cursor() as cur:
        cur.execute(sql, params)    
        res = cur.fetchall()
        return [dict(res[i]) for i in range(len(res))]

def execute(sql, **params):
    with get_cursor() as cur:
        cur.execute(sql, params)


def commit():
	if hasattr(flask.g,'dbconn'):
		conn = flask.g.dbconn
		conn.commit()
		close()

def rollback():
	if hasattr(flask.g,'dbconn'):
		conn = flask.g.dbconn
		conn.rollback()
		close()

def close():
    if hasattr(flask.g, 'dbconn'):
        conn = flask.g.dbconn
        conn.close()
        delattr(flask.g, 'dbconn')



