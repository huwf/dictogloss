"""
This module is for places where I have customised various other libraries
Or where this app could conceivably be customised in the future.
"""
from flask_security import LoginForm
from flask_security.forms import get_form_field_label, password_required
from flask_security.utils import get_message, _datastore, login_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField
# from flask_oauthlib.provider import OAuth2Provider
from flask_login import LoginManager



# TODO: Still doesn't work properly.
class ExtendedLoginForm(LoginForm):
    # New field
    username = StringField('Username')
    # We don't want email to be compulsory
    email = StringField(get_form_field_label('email'))

    def validate(self):
        if not super(ExtendedLoginForm, self).validate():
            return False

        self.user = _datastore.get_user(self.username.data)
        if self.user is None:
            self.username.errors.append(get_message('USER_DOES_NOT_EXIST')[0])
            return False


# class