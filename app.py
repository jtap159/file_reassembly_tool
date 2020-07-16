import flask
from flask import request
import tasks

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
    assembled_fragments = tasks.assemble_frags(frags)
    if type(assembled_fragments) == str:
        return assembled_fragments
    else:
        comment = f"{len(assembled_fragments)} Possible Solutions Found (see solutions below) \n\n"
        assembled_solutions = comment
        for i, solution in enumerate(assembled_fragments):
            separation = f"-----------------------Solution {i + 1}---------------------------------- \n\n"
            show_solution = separation + solution
            assembled_solutions = assembled_solutions + show_solution + "\n"
        return assembled_solutions


if __name__ == "__main__":
    app.run()

