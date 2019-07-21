
from flask import jsonify

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

import sqlalchemy as db

pages = Blueprint('pages', __name__)

# [START list]
@pages.route("/booking")
def main_page():
    return render_template(
        "booking.html")

@pages.route("/getBooking")
def get_booking():
    booking_list = {"data":[{"Id": '1',
                           "ClientName": 'XXX1',
                           "Date":'2019-05-01',
                           "SalesRep":'SP1'},
                          {"Id": '2',
                           "ClientName": 'XXX2',
                           "Date": '2019-05-09',
                           "SalesRep": 'SP2'},
                          ]}
    return jsonify(booking_list)


@pages.route("/venue")
def venues():
    return render_template("venues.html")

@pages.route("/getVenue")
def get_venues():
    venue_list = {"data":[{"VenueName": 'One',
                           "Address": 'One Victoria Street South',
                           "City":'Kitchener',
                           "Country":'Canada',
                           "Price":1000,
                           "PostalCode": 'N2G0B5'},
                          {"VenueName": 'Two',
                           "Address": 'Two Victoria Street South',
                           "City": 'Kitchener',
                           "Country": 'Canada',
                           "Price": 1200,
                           "PostalCode": 'N2G0X5'}
                          ]}
    return jsonify(venue_list)


@pages.route("/client")
def client():
    return render_template("client.html")

@pages.route("/getClient")
def get_client():
    client_list = {"data":[{"ClientName": 'Frank Xu',
                           "Address": 'One Victoria Street South',
                           "City":'Kitchener',
                           "Country":'Canada',
                           "PostalCode": 'N2G0B5'},
                          {"ClientName": 'Weixuan Xu',
                           "Address": 'Two Victoria Street South',
                           "City": 'Kitchener',
                           "Country": 'Canada',
                           "PostalCode": 'N2G0X5'}
                          ]}
    return jsonify(client_list)

@pages.route("/supplier")
def supplier():
    token = request.args.get('page_token',None)
    return render_template("supplier.html")

@pages.route("/myaccount")
def myaccount():
    token = request.args.get('page_token',None)
    return render_template("myaccount.html")