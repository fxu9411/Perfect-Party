
from flask import jsonify

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

import sqlalchemy as db

pages = Blueprint('pages', __name__)

# [START list]
@pages.route("/booking")
def main_page():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    #books, next_page_token = get_model().list(cursor=token)

    return render_template(
        "booking.html")
        #books=books,
        #next_page_token=next_page_token)
# [END list]

@pages.route("/venue")
def venues():
    return render_template("venues.html")

@pages.route("/getVenue")
def get_venues():
    venue_list = {"data":[{"VenueName": 'One', "Address": 'One Victoria Street South', "City":'Kitchener', "Country":'Canada',"Price":1000}]}
    return jsonify(venue_list)


@pages.route("/client")
def client():
    token = request.args.get('page_token',None)
    return render_template("client.html")

@pages.route("/supplier")
def supplier():
    token = request.args.get('page_token',None)
    return render_template("supplier.html")

@pages.route("/myaccount")
def myaccount():
    token = request.args.get('page_token',None)
    return render_template("myaccount.html")