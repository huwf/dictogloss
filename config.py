"""
This file contains all configuration required for the Flask app.
Also used is Flask Security, and so can contain configuration options for that
and all other libraries in it as well.
"""

SECRET_KEY = 'b22699b99d57bca24f8c506e4b04c12e'
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = '5db81de85853b1b699e24086e4d3ce0b'
SECURITY_USER_IDENTITY_ATTRIBUTES = 'username'
