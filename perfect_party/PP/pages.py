
from flask import jsonify

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

import pymysql

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
    connection = pymysql.connect(host='127.0.0.1',
                                 user='admin',
                                 password='password',
                                 db='perfect_party',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `venue`"
        cursor.execute(sql)
        result = cursor.fetchall()

    venue_list = {}
    list_of_venue = []
    for item in result:
        obj = {'VenueName': item['venue_name'],
               'Address': item['street_number'] + ' ' + item['street_name'],
               'City': item['city'], 'Country': item['country'], 'PostalCode': item['postal_code'],
               'Price': item['price']}
        list_of_venue.append(obj)

    venue_list['data'] = list_of_venue
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