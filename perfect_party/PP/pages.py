

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

pages = Blueprint('pages', __name__)

# [START list]
@pages.route("/")
def main_page():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    #books, next_page_token = get_model().list(cursor=token)

    return render_template(
        "main_page.html")
        #books=books,
        #next_page_token=next_page_token)
# [END list]