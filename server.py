import os
from flask import Flask, request
app = Flask(__name__)

@app.route('/python', methods=['POST'])
def python_command():
    return str(eval(request.form['text']))

if __name__ == '__main__':
    host = os.environ.get('IP', '127.0.0.1')
    port = os.environ.get('PORT', 5000)
    
    app.run(host=host, port=int(port), debug=__debug__)
