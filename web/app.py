import io
from run import run
from flask import Flask, render_template, request
import sys
sys.path.insert(0, '..')


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/playground')
def playground():
    return render_template("playground.html")


@app.route('/process', methods=['POST'])
def process():
    text = request.form['code'].strip()
    if len(text) < 1:
        logs = "Empty Code"
        return render_template('playground.html', result=logs)
    # Redirect standard output to capture logs
    log_output = io.StringIO()
    sys.stdout = log_output

    result, error = run(text)

    # Reset standard output to original
    sys.stdout = sys.__stdout__

    logs = log_output.getvalue()
    if logs == "":
        if not result:
            logs = error.msg_as_string()
        else:
            logs = result
    log_output.close()
    logs = logs.split('\n')
    return render_template('playground.html', result=logs)


if __name__ == '__main__':
    app.run(debug=True)
