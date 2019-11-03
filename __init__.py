from flask import Flask

app = Flask(__name__)
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
