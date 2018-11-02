import psycopg2
import psycopg2.extras
import flask
from . import config

def get_connection():
    if not hasattr(flask.g, 'dbconn'):
        flask.g.dbconn = psycopg2.connect(
            database = config.DB_NAME,        
            host     = config.DB_HOST,
            user     = config.DB_USER,
            port     = config.DB_PORT,
            password = config.DB_PASS)
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


def _rollback_db(sender, exception, **extra):
    if hasattr(flask.g, 'dbconn'):
        conn = flask.g.dbconn
        conn.rollback()
        conn.close()
        delattr(flask.g, 'dbconn')

def _commit_db():
    if hasattr(flask.g, 'dbconn'):
        conn = flask.g.dbconn
        conn.commit()





