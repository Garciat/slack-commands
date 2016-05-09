import io
import os
import dis
import sys
import threading
import traceback

from contextlib import contextmanager

from flask import Flask, request

app = Flask(__name__)


statement_lock = threading.Lock()


def run_statement(src):
    with statement_lock, io.BytesIO() as out_buffer, redirect_stdout(out_buffer):
        exec(src)
        return out_buffer.getvalue()


def run_expression(src):
    return eval(src)


def dis_statement(src):
    with statement_lock, io.BytesIO() as out_buffer, redirect_stdout(out_buffer):
        dis.dis(compile(src, '<slack>', 'exec'))
        return out_buffer.getvalue()


def dis_expression(src):
    with statement_lock, io.BytesIO() as out_buffer, redirect_stdout(out_buffer):
        dis.dis(compile(src, '<slack>', 'eval'))
        return out_buffer.getvalue()


code_handlers = [
    ('@!', dis_statement),
    ('@', dis_expression),
    ('!', run_statement),
    ('', run_expression),  # default. last because empty prefix
]


@app.route('/python', methods=['POST'])
def python_command():
    src = request.form['text']
    
    if not src:
        return 'Empty snippet ):'
    
    try:
        output = None

        for prefix, handler in code_handlers:
            if src.startswith(prefix):
                src_clean = src[len(prefix):]
                output = handler(src_clean)
                break

        return "```{}```".format(output)
    except:
        traceback.print_exc()
        return 'Your snippet failed ):'


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
