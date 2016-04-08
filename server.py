from flask import Flask, request
from flask_slack import Slack

app = Flask(__name__)

slack = Slack(app)

@slack.command('python', token='UfzxmsQwTovzkgJnC4lk9KFj', methods=['POST'])
def python_command(**kwargs):
    text = kwargs.get('text')
    return slack.response(eval(text))

if __name__ == '__main__':
    app.run()
