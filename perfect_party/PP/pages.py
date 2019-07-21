
from flask import jsonify,json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

import pymysql

pages = Blueprint('pages', __name__)

connection = pymysql.connect(host='127.0.0.1',
                             user='admin',
                             password='password',
                             db='perfect_party',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# [START list]
@pages.route("/booking", methods=['POST','GET'])
def main_page():
    if request.method == 'POST':
        args = json.loads(request.values.get("args"))
        booking_id = int(args['Id'])
        return redirect(url_for('pages.one_book',Id=args['Id']))
    return render_template(
        "booking.html")

@pages.route("/getBooking")
def get_booking():
    with connection.cursor() as cursor:
        sql = "SELECT booking.booking_id, client.client_name, DATE(booking.booking_date) as booking_date, booking.sales_rep " \
              "FROM `perfect_party`.`booking`" \
              "LEFT JOIN `perfect_party`.`event` as event USING (event_id)" \
              "LEFT JOIN `perfect_party`.`client` as client ON event.client_id = client.client_id"
        cursor.execute(sql)
        result = cursor.fetchall()

    booking_list = {}
    list_of_booking = []
    for item in result:
        obj = {'Id': item['booking_id'],
               'ClientName': item['client_name'],
               'Date': str(item['booking_date']),
               'SalesRep': item['sales_rep']}
        list_of_booking.append(obj)

    booking_list['data'] = list_of_booking
    return jsonify(booking_list)

@pages.route("/onebook", methods=['POST','GET'])
def one_book():
    if request.method == 'POST':
        args = json.loads(request.values.get("args"))
        booking_id = int(args['Id'])
        print(booking_id)
        return jsonify({'data': args['Id']})
    else:
        return render_template('onebook.html')


@pages.route("/postBooking", methods=['POST'])
def get_id():

    args = json.loads(request.values.get("args"))
    client_list = {"data": [{"ClientName": 'Frank Xu',
                             "Address": 'One Victoria Street South',
                             "City": 'Kitchener',
                             "Country": 'Canada',
                             "PostalCode": 'N2G0B5'},
                            {"ClientName": 'Weixuan Xu',
                             "Address": 'Two Victoria Street South',
                             "City": 'Kitchener',
                             "Country": 'Canada',
                             "PostalCode": 'N2G0X5'}
                            ]}
    booking_id = int(args['Id'])
    return jsonify(client_list)


@pages.route("/venue")
def venues():
    return render_template("venues.html")

@pages.route("/schema")
def schema():
    with connection.cursor() as cursor:
        sql = "SHOW TABLES"
        cursor.execute(sql)
        tables = cursor.fetchall()
    s = []
    for row in tables:
        table = row["Tables_in_perfect_party"]
        with connection.cursor() as cursor:
            sql = f'DESCRIBE `{table}`'
            cursor.execute(sql)
            cols = cursor.fetchall()
        s.append({table: cols})
    return jsonify(s)

@pages.route("/getVenue")
def get_venues():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `venue`"
        cursor.execute(sql)
        result = cursor.fetchall()

    venue_list = {}
    list_of_venue = []
    for item in result:
        obj = {'VenueName': item['venue_name'],
               'Address': item['street_number'] + ' ' + item['street_name'],
               'City': item['city'],
               'Country': item['country'],
               'PostalCode': item['postal_code'],
               'Price': float(item['price'])}
        list_of_venue.append(obj)
    # cursor.close()
    venue_list['data'] = list_of_venue
    return jsonify(venue_list)

@pages.route('/addVenue', methods=['POST'])
def add_venue():
    print(request.form)
    name = request.form['name']
    str_name = request.form['str-name']
    str_number = request.form['str-number']
    unit_number = request.form['unit'] if 'unit' in request.form else 'NULL'
    city = request.form['city']
    province = request.form['province']
    country = request.form['country']
    postal = request.form['postal']
    price = request.form['price']

    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `venue`(venue_name, street_number, street_name, unit_number, city, province, country, postal_code, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (name, str_number, str_name, unit_number, city, province, country, postal, price))
    connection.commit()

    return redirect(url_for('pages.venues'))

@pages.route("/client")
def client():
    return render_template("client.html")

@pages.route("/getClient")
def get_client():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `client`"
        cursor.execute(sql)
        result = cursor.fetchall()

    client_list = {}
    list_of_client = []
    for item in result:
        obj = {'ClientName': item['client_name'],
               'Address': item['street_number'] + ' ' + item['street_name'],
               'City': item['city'], 'Country': item['country'], 'PostalCode': item['postal_code']}
        list_of_client.append(obj)

    client_list['data'] = list_of_client
    return jsonify(client_list)

@pages.route('/addClient', methods=['POST'])
def add_client():
    print(request.form)
    name = request.form['name']
    str_name = request.form['str-name']
    str_number = request.form['str-number']
    unit_number = request.form['unit'] if 'unit' in request.form else 'NULL'
    city = request.form['city']
    province = request.form['province']
    country = request.form['country']
    postal = request.form['postal']

    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `client`(client_name, street_number, street_name, unit_number, city, province, country, postal_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (name, str_number, str_name, unit_number, city, province, country, postal))
    connection.commit()

    return redirect(url_for('pages.client'))

@pages.route("/supplier")
def supplier():
    return render_template("supplier.html")

@pages.route("/getSupplier")
def get_supplier():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `supplier`"
        cursor.execute(sql)
        result = cursor.fetchall()

    supplier_list = {}
    list_of_supplier = []
    for item in result:
        obj = {'Supplier ID': item['supplier_id'],
               'Name': item['name'],
               'Phone Number': item['phone_number'],
               'Type': item['type']}
        list_of_supplier.append(obj)

    supplier_list['data'] = list_of_supplier

    return jsonify(supplier_list)



@pages.route("/myaccount")
def myaccount():
    token = request.args.get('page_token',None)
    return render_template("myaccount.html")
