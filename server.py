import io
import os
import sys
import threading
import traceback

from contextlib import contextmanager

from flask import Flask, request

app = Flask(__name__)

@app.route('/python', methods=['POST'])
def python_command():
    src = request.form['text']
    
    if not src:
        return 'Empty snippet ):'
    
    is_statement = src.startswith('!')
    
    try:
        output = None
        if is_statement:
            src = src[1:]
            output = run_statement(src)
        else:
            output = run_expression(src)
        return str(output)
    except:
        traceback.print_exc()
        return 'Your snippet failed ):'


statement_lock = threading.Lock()


def run_statement(src):
    with statement_lock, io.BytesIO() as out_buffer, redirect_stdout(out_buffer):
        exec(src)
        return out_buffer.getvalue()


def run_expression(src):
    return eval(src)


@contextmanager
def redirect_stdout(stream, stdout=True, stderr=False):
    """
    https://github.com/jackkamm/redirect_stdout2
    """
    if stdout:
        sys.stdout = stream
    if stderr:
        sys.stderr = stream
    try:
        yield
    except Exception,e:
        if stderr:
            traceback.print_exc()
        raise
    finally:
        if stdout:
            sys.stdout = sys.__stdout__
        if stderr:
            sys.stderr = sys.__stderr__


if __name__ == '__main__':
    host = os.environ.get('IP', '0.0.0.0')
    port = os.environ.get('PORT', 5000)
    
    app.run(host=host, port=int(port), debug=__debug__)
