from app import app
from flask import request, abort, jsonify

@app.route('/')
@app.route('/<string:name>/')
def index(name = "pomidorka"):
    return "Hello, {}!".format(name)

@app.route('/form/', methods=['GET', 'POST'])
def form():
    if request.method == "GET":
        return """<html><head></head><body>
        <form method="POST" action="/form/">
            <input name="first_name">
            <input name="last_name">
            <input type="submit">
        </form></body></html>"""
    else:
        rv = jsonify(request.form)
        return rv
