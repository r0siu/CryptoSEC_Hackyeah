from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from backend.jwt.AuthenticationService import AuthenticationService


app = Flask(__name__)
CORS(app)

API_VERSION_PREFIX = '/api/v1'

DOCUMENT_RESOURCE = '/document'

authService = AuthenticationService()

# region login

# TODO: Mocked endpoint with no functionality whatsoever - needs implementation
@app.route(API_VERSION_PREFIX + '/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    jwt = authService.authenticate_user(username, password)

    return jsonify({'jwt': jwt})

# endregion

# region document
# TODO: this is a mocked method - it need an implementation
@app.route(API_VERSION_PREFIX + DOCUMENT_RESOURCE + '/encrypt', methods=['POST'])
def encrypt_document():
    receivedDocument = request.files['file']
    if receivedDocument:
        receivedDocument.save(receivedDocument.filename)
        return send_file(receivedDocument.filename, as_attachment=True)


@app.route(API_VERSION_PREFIX + DOCUMENT_RESOURCE + '/decrypt', methods=['POST'])
def decrypt_document():
    receivedDocument = request.files['file']
    if receivedDocument:
        receivedDocument.save(receivedDocument.filename)
        return send_file(receivedDocument.filename, as_attachment=True)


@app.route(API_VERSION_PREFIX + DOCUMENT_RESOURCE + '/sign', methods=['POST'])
def sign_document():
    receivedDocument = request.files['file']
    if receivedDocument:
        receivedDocument.save(receivedDocument.filename)
        return send_file(receivedDocument.filename, as_attachment=True)


@app.route(API_VERSION_PREFIX + DOCUMENT_RESOURCE + '/verify', methods=['POST'])
def verify_document():
    return jsonify({'is_valid': True})


# endregion


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
