from flask import jsonify, json
from datetime import datetime

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
def main_page():
    return booking


@pages.route("/booking", methods=['POST', 'GET'])
def booking():
    if request.method == 'POST':
        args = json.loads(request.values.get("args"))
        booking_id = int(args['Id'])
        return redirect(url_for('pages.one_book', Id=args['Id']))
    with connection.cursor() as cursor:
        sql = "SELECT * " \
            "FROM `venue`"
        cursor.execute(sql)
        venues = cursor.fetchall()
    with connection.cursor() as cursor:
        sql = "SELECT * " \
            "FROM `client`"
        cursor.execute(sql)
        clients = cursor.fetchall()
    return render_template("booking.html", booking=True, venues=venues, clients=clients)


@pages.route("/getBooking")
def get_booking():
    with connection.cursor() as cursor:
        sql = "SELECT booking.booking_id, client.client_name, DATE(booking.booking_date) as booking_date, booking.sales_rep, " \
              "DATE(event.event_date) as event_date, venue.venue_name " \
              "FROM `perfect_party`.`booking` as booking " \
              "LEFT JOIN `perfect_party`.`event` as event USING (event_id) " \
              "LEFT JOIN `perfect_party`.`client` as client ON booking.client_id = client.client_id " \
              "LEFT JOIN `perfect_party`.`venue` as venue ON event.venue_id = venue.venue_id "
        cursor.execute(sql)
        result = cursor.fetchall()

    booking_list = {}
    list_of_booking = []
    for item in result:
        print(item)
        obj = {'ID': item['booking_id'],
               'ClientName': item['client_name'],
               'Date': str(item['booking_date']),
               'SalesRep': item['sales_rep'],
               'Venue': item['sales_rep'],
               'EventDate': str(item['event_date']),
               'VenueName': str(item['venue_name']),}
        list_of_booking.append(obj)

    booking_list['data'] = list_of_booking
    return jsonify(booking_list)


@pages.route('/addBooking', methods=['POST'])
def add_booking():
    print(request.form)
    tpe = request.form['type']
    guests = request.form['guests']
    budget = request.form['budget']
    date = request.form['date']
    venue_id = request.form['venue_id']
    client_id = request.form['client_id']
    sales_rep = request.form['sales_rep']

    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `event`(venue_id, guest_number, event_date, budget, type) VALUES (%s, %s, %s, %s, %s)"
        result = cursor.execute(sql, (venue_id, guests, date, budget, tpe))
        event_id = connection.insert_id()
    connection.commit()

    print('event_id = ', event_id)
    booking_date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `booking`(event_id, client_id, sales_rep, booking_date) VALUES (%s, %s, %s, %s)"
        result = cursor.execute(sql, (event_id, client_id, sales_rep, booking_date))
    connection.commit()

    return redirect(url_for('pages.booking'))


@pages.route("/onebook", methods=['GET'])
def get_book():
    booking_id = request.args.get('booking_id')
    print('booking_id = ', booking_id)
    with connection.cursor() as cursor:
        sql = "SELECT booking.booking_id, client.client_name, DATE(booking.booking_date) as booking_date, booking.sales_rep, " \
              "DATE(event.event_date) as event_date, venue.venue_name, event.type " \
              "FROM `perfect_party`.`booking` as booking " \
              "LEFT JOIN `perfect_party`.`event` as event USING (event_id) " \
              "LEFT JOIN `perfect_party`.`client` as client ON booking.client_id = client.client_id " \
              "LEFT JOIN `perfect_party`.`venue` as venue ON event.venue_id = venue.venue_id " \
              f"WHERE `booking_id`='{booking_id}' "
        cursor.execute(sql)
        result = cursor.fetchone()
    print(result)
    return render_template("onebook.html", onebook=True, result=result)

@pages.route("/postBooking", methods=['POST'])
def get_id():
    args = json.loads(request.values.get("args"))
    booking_id = int(args['Id'])
    return jsonify(booking_id)


@pages.route("/venue")
def venue():
    return render_template("venue.html", venue=True)

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
               'Price': float(item['price']),
               'ID': item['venue_id'],
               'Street_Number': item['street_number'],
               'Street_Name': item['street_name'],
               'Unit_Number': item['unit_number']}
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

    return redirect(url_for('pages.venue'))


@pages.route('/editVenue', methods=['POST'])
def edit_venue():
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
    id = request.form['id']

    with connection.cursor() as cursor:
        sql = "UPDATE `client` SET client_name = %s, street_number = %s, street_name = %s, " \
              "unit_number = %s, city = %s, province = %s, country = %s, postal_code = %s " \
              "WHERE client_id = %d;" % (repr(name), repr(str_number), repr(str_name), repr(unit_number),
                                         repr(city), repr(province), repr(country), repr(postal), int(id))
        print(sql)
        cursor.execute(sql)
        connection.commit()
        cursor.close()
    return redirect(url_for('pages.client'))


@pages.route('/deleteVenue', methods=['POST'])
def delete_venue(): \
        # implementation here
    print(request.form)
    id = request.form['id']

    with connection.cursor() as cursor:
        sql = "DELETE FROM `venue` WHERE venue_id = %d;" % int(id)
        print(sql)
        cursor.execute(sql)
        connection.commit()
        cursor.close()

    return redirect(url_for('pages.client'))

@pages.route("/client")
def client():
    return render_template("client.html", client=True)


@pages.route("/getClient")
def get_client():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `client`"
        cursor.execute(sql)
        result = cursor.fetchall()

    client_list = {}
    list_of_client = []
    for item in result:
        if item['unit_number'] == None:
            obj = {'ClientName': item['client_name'],
                   'Address': item['street_number'] + ' ' + item['street_name'],
                   'City': item['city'],
                   'Province': item['province'],
                   'Country': item['country'],
                   'PostalCode': item['postal_code'],
                   'Unit': item['unit_number'],
                   'Street_Number': item['street_number'],
                   'Street_Name': item['street_name'],
                   'Client_ID': item['client_id']}
        else:
            obj = {'ClientName': item['client_name'],
                   'Address': item['unit_number'] + '-' + item['street_number'] + ' ' + item['street_name'],
                   'City': item['city'],
                   'Province': item['province'],
                   'Country': item['country'],
                   'PostalCode': item['postal_code'],
                   'Unit': item['unit_number'],
                   'Street_Number': item['street_number'],
                   'Street_Name': item['street_name'],
                   'Client_ID': item['client_id']}
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


@pages.route('/editClient', methods=['POST'])
def edit_client():
    print(request.form)
    name = request.form['name']
    str_name = request.form['str-name']
    str_number = request.form['str-number']
    unit_number = request.form['unit'] if 'unit' in request.form else 'NULL'
    city = request.form['city']
    province = request.form['province']
    country = request.form['country']
    postal = request.form['postal']
    id = request.form['id']

    with connection.cursor() as cursor:
        sql = "UPDATE `client` SET client_name = %s, street_number = %s, street_name = %s, " \
              "unit_number = %s, city = %s, province = %s, country = %s, postal_code = %s " \
              "WHERE client_id = %d;" % (repr(name), repr(str_number), repr(str_name), repr(unit_number),
                                         repr(city), repr(province), repr(country), repr(postal), int(id))
        print(sql)
        cursor.execute(sql)
        connection.commit()
        cursor.close()
    return redirect(url_for('pages.client'))

@pages.route('/deleteClient', methods=['POST'])
def delete_client():\
    #implementation here
    print(request.form)
    id = request.form['id']

    with connection.cursor() as cursor:
        sql = "DELETE FROM `client` WHERE client_id = %d;" % int(id)
        print(sql)
        cursor.execute(sql)
        connection.commit()
        cursor.close()

    return redirect(url_for('pages.client'))


@pages.route("/supplier")
def supplier():
    return render_template("supplier.html", supplier=True)


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


@pages.route('/editSupplier', methods=['POST'])
def edit_supplier():
    print(request.form)
    name = request.form['name']
    phone_number = request.form['phone']  # wait for the form
    type = request.form['type']
    id = request.form['id']

    with connection.cursor() as cursor:
        sql = "UPDATE `supplier` SET name = %s, phone_number = %s, type = %s " \
              "WHERE supplier_id = %d;" % (repr(name), repr(phone_number), repr(type), int(id))
        print(sql)
        cursor.execute(sql)
        connection.commit()
        cursor.close()
    return redirect(url_for('pages.supplier'))

@pages.route('/addSupplier', methods=['POST'])
def add_supplier():
    print(request.form)
    name = request.form['name']
    phone = request.form['phone']
    tpe = request.form['type']

    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `supplier`(name, phone_number, type) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, phone, tpe))
    connection.commit()

    return redirect(url_for('pages.supplier'))


@pages.route('/deleteSupplier', methods=['POST'])
def delete_supplier():
    print(request.form)
    id = request.form['id']

    with connection.cursor() as cursor:
        sql = "DELETE FROM `supplier` WHERE supplier_id = %d;" % int(id)
        print(sql)
        cursor.execute(sql)
        connection.commit()
        cursor.close()
    return redirect(url_for('pages.supplier'))

@pages.route("/item/getitem")
def get_item():
    item=request.args.get('item')
    with connection.cursor() as cursor:
        sql = "SELECT *" \
              "FROM `perfect_party`.`item_option` as item " \
              "LEFT JOIN `perfect_party`.`supplier` as supplier " \
              "ON item.supplier_id = supplier.supplier_id " \
              f"WHERE type = '{item}'"
        cursor.execute(sql)
        result = cursor.fetchall()

    food_list = {}
    list_of_food = []
    for item in result:
        obj = {'ID': item['item_id'],
               'Name': item['name'],
               'Price': str(item['price']),
               'Supplier ID': item['supplier.supplier_id'],
               'Supplier Name': item['supplier.name'],
               'Type': item['type']}
        list_of_food.append(obj)

    food_list['data'] = list_of_food

    return jsonify(food_list)

@pages.route('/addItem', methods=['POST'])
def add_item():
    print(request.form)
    item = request.args.get('item')
    name = request.form['name']
    price = request.form['price']
    supplier_id = request.form['supplier_id']

    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `item_option`(name, price, supplier_id) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, price, supplier_id))
    connection.commit()

    return redirect(url_for(f'pages.item_{item.lower()}'))

def item(item):
    with connection.cursor() as cursor:
        sql = "SELECT * " \
            "FROM `supplier` " \
            f"WHERE type='{item}'"
        cursor.execute(sql)
        result = cursor.fetchall()
    return render_template("item.html", item=item, suppliers=result)


@pages.route("/item/food")
def item_food():
    return item('Food')


@pages.route("/item/decor")
def item_decor():
    return item('Decor')


@pages.route("/item/entertainment")
def item_entertainment():
    return item('Entertainment')


@pages.route("/myaccount")
def myaccount():
    token = request.args.get('page_token', None)
    return render_template("myaccount.html")


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
