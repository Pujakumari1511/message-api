import flask
import controllerHelper as helper
from flask import request
from json5 import dumps
from dicttoxml import dicttoxml
from Message import Message

app = flask.Flask(__name__)
app.config['DEBUG'] = True
messages = []   # array for saving messages


@app.route('/', methods=['GET'])
def home():
    return '<h1>Create your messages</h1>'


@app.route('/api/create/message', methods=['POST'])
def create_message():
    if 'title' in request.json and 'content' in request.json and 'sender' in request.json and 'url' in request.json:
        title = request.json['title']
        content = request.json['content']
        sender = request.json['sender']
        url = request.json['url']
        if helper.is_length_incorrect(title, content, sender):
            return "Error: all fields length should be smaller than 30"

        if helper.is_url_incorrect(url):
            return "Error: url is invalid", 400
        message = Message(title, content, sender, url)
        messages.append(message)
        return "Success: message is saved", 200
    else:
        return "Error: request body has invalid json", 400


@app.route('/api/read/messages', methods=['GET'])
def read_all_messages():
    if 'version' in request.args and request.args['version'] == "1":
        return dumps(list(map(Message.get_message_in_dict_for_v1, messages)))
    elif 'version' in request.args and request.args['version'] == "2":
        if 'format' in request.args:
            result = list(map(Message.get_message_in_dict_for_v2, messages))
            data_format = request.args['format']
            if data_format == 'json':
                return dumps(result)
            elif data_format == 'xml':
                return dicttoxml(result, custom_root='messages', attr_type=False)
            else:
                return "Error: Invalid format, provide either json or xml", 400
        else:
            return "Error: please provide format parameter", 400
    else:
        return "Error: Invalid version, valid version are 1 and 2", 400


if __name__ == "__main__":
    app.run()
