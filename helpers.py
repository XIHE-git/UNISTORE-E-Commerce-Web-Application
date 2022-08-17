import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField

"""
login_required --- A decrator which decorate f function. It requires users to login in order to visit some pages.

@return:
    redirect to login route or return f after decoration
"""
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


"""
AccountUpdateForm --- A Python class for updating profile picture form

@return:
    NONE
"""
class AccountUpdateForm(FlaskForm):
    picture = FileField(label = "Update Profile Picture", validators = [FileAllowed(['jpg','png'])])
    submit = SubmitField(label = "Update")

"""
AccountUpdateForm --- A Python class for updating product picture form

@return:
    None
"""
class ProductUpdate(FlaskForm):
    picture = FileField(label = "Update a Product Picture", validators = [FileAllowed(['jpg','png'])])
    submit = SubmitField(label = "Update")

"""
usd --- A Python function convert input to USD format

@return:
    USD format string
"""
def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
