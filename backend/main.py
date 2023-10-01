import io

from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS

from backend.auth.AuthenticationService import AuthenticationService
from backend.crypto.aes import Aes

app = Flask(__name__)
CORS(app, expose_headers=["Content-Disposition"])

API_VERSION_PREFIX = '/api/v1'

DOCUMENT_RESOURCE = '/document'

authService = AuthenticationService()

aes = Aes()
aes.generate_aes_key()

# region login

# TODO: returns only generated JWT, we need to implement a repository to check username/password and pass scopes to JWT
@app.route(API_VERSION_PREFIX + '/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    jwt = authService.authenticate_user(username, password)

    return jsonify({'auth': jwt})

# endregion

# region document
# TODO: this is a mocked method - it need an implementation
@app.route(API_VERSION_PREFIX + DOCUMENT_RESOURCE + '/encrypt', methods=['POST'])
def encrypt_document():
    received_document = request.files['file']
    mode = request.form.get('choice')
    if received_document:
        binary_data = received_document.read()
        encrypted_document = aes.encrypt(binary_data, mode)
        response = send_file(io.BytesIO(encrypted_document), as_attachment=True, download_name=received_document.filename + '_encrypted_' + mode, mimetype='application/octet-stream')
        response.headers['mode'] = mode
        return response


@app.route(API_VERSION_PREFIX + DOCUMENT_RESOURCE + '/decrypt', methods=['POST'])
def decrypt_document():
    received_document = request.files['file']
    mode = request.form.get('choice')
    if received_document:
        binary_data = received_document.read()
        decrypted_document = aes.decrypt(binary_data, mode)
        response = send_file(io.BytesIO(decrypted_document), as_attachment=True, download_name=received_document.filename, mimetype='application/octet-stream')
        response.headers['mode'] = mode
        return response


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
