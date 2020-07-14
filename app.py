import flask
from flask import request, jsonify
import json
from tasks.reassemble import assemble_frags

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def home():
    return '''<h1>KBase Challange</h1>'''


@app.route('/reassemble_frags', methods=['POST'])
def reassemble_frags():
    # frags = request.args['fragments']
    frags = request.args['fragments']
    frags = frags.split(",,, ")
    assembled_fragments = assemble_frags(frags)
    return assembled_fragments


if __name__ == "__main__":
    app.run()

