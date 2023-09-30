from flask import Flask, request, jsonify

app = Flask(__name__)

API_VERSION_PREFIX = '/api/v1'

DOCUMENT_RESOURCE = '/document'


# region login

# TODO: this method should be accessible form authentication server
@app.route(API_VERSION_PREFIX + '/login', methods=['POST'])
def login_user():
    return jsonify({'message': 'ok'})

# endregion

# region document
@app.route(API_VERSION_PREFIX + DOCUMENT_RESOURCE + '/encrypt', methods=['POST'])
def encrypt_document():
    return jsonify({'message': 'ok'})

@app.route(API_VERSION_PREFIX + DOCUMENT_RESOURCE + '/decrypt', methods=['POST'])
def decrypt_document():
    return jsonify({'message': 'ok'})

@app.route(API_VERSION_PREFIX + DOCUMENT_RESOURCE + '/sign', methods=['POST'])
def sign_document():
    return jsonify({'message': 'ok'})

@app.route(API_VERSION_PREFIX + DOCUMENT_RESOURCE + '/verify', methods=['POST'])
def verify_document():
    return jsonify({'message': 'ok'})


# endregion


if __name__ == '__main__':
    app.run(debug=True)
