import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def home():
    return '''<h1>KBase Challange</h1>'''


@app.route('/reassemble_frags', methods=['POST'])
def reassemble_frags():
    frags = request.args['fragments']
    print(type(frags))
    return frags


if __name__ == "__main__":
    app.run()
