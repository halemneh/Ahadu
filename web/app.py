from flask import Flask, render_template
from flask_socketio import SocketIO, send
# from run import run
from sys import stdout
from io import StringIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('message')
def run(messgae):
    print('Recieved: ' + messgae)
# def runCode(code):
#     log_prints = StringIO()
#     stdout - log_prints

#     _, error = run(code)
#     if error:
#         return error.msg_as_string()
#     log = log_prints.getvalue()
#     log_prints.close()
#     return log

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/playground')
def playground():
    return render_template("playground.html")


# @app.route('/process', methods=['POST'])
# def process():
#     text = request.form['code'].strip()
#     # Redirect standard output to capture logs
#     log_output = io.StringIO()
#     sys.stdout = log_output

#     result, error = run(text)

#     # Reset standard output to original
#     sys.stdout = sys.__stdout__

#     logs = log_output.getvalue()
#     if logs == "":
#         if not result:
#             logs = error.msg_as_string()
#         else:
#             logs = result
#     log_output.close()
#     return render_template('index.html', result=logs)

if __name__ == '__main__':
    socketio.run(app, debug=True)
