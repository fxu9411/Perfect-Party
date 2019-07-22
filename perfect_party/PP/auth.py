

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

auth = Blueprint('auth', __name__)

@auth.route("/")
def sign_in():
    item = request.form['inputEmail']
    print(item)
    return render_template(
        "sign-in.html")
