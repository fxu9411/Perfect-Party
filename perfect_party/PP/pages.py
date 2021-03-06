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
        cursor.close()
    with connection.cursor() as cursor:
        sql = "SELECT * " \
              "FROM `client`"
        cursor.execute(sql)
        clients = cursor.fetchall()
        cursor.close()
    return render_template("booking.html", booking=True, venues=venues, clients=clients)


@pages.route("/getBooking")
def get_booking():
    with connection.cursor() as cursor:
        sql = "SELECT booking.booking_id, client.client_name, DATE(booking.booking_date) as booking_date, booking.sales_rep, " \
              "DATE(event.event_date) as event_date, venue.venue_name " \
              "FROM `perfect_party`.`booking` as booking " \
              "LEFT JOIN `perfect_party`.`event` as event USING (event_id) " \
              "LEFT JOIN `perfect_party`.`client` as client ON booking.client_id = client.client_id " \
              "LEFT JOIN `perfect_party`.`venue` as venue ON event.venue_id = venue.venue_id " \
              "WHERE booking.is_deleted = 0"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()


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
               'VenueName': str(item['venue_name']), }
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
              "DATE(event.event_date) as event_date, venue.venue_name, event.type, event.guest_number, event.budget, event.event_id " \
              "FROM `perfect_party`.`booking` as booking " \
              "LEFT JOIN `perfect_party`.`event` as event USING (event_id) " \
              "LEFT JOIN `perfect_party`.`client` as client ON booking.client_id = client.client_id " \
              "LEFT JOIN `perfect_party`.`venue` as venue ON event.venue_id = venue.venue_id " \
             f"WHERE `booking_id`='{booking_id}' "
        cursor.execute(sql)
        result = cursor.fetchone()
        # print(result)
        cursor.close()
    event_id = result['event_id']
    print('event_id = ', event_id)

    with connection.cursor() as cursor:
        sql = "SELECT *, DATE(ordered_item.`order_date`) AS ordered_date " \
            "FROM perfect_party.ordered_item AS ordered_item " \
            "LEFT JOIN perfect_party.event AS event " \
            "  ON ordered_item.`event_id`=event.`event_id` " \
            "LEFT JOIN perfect_party.item_option AS item_option " \
            "  ON ordered_item.`item_id`=item_option.`item_id` " \
            "LEFT JOIN perfect_party.supplier AS supplier " \
            "  ON item_option.`supplier_id`=supplier.`supplier_id` " \
           f"WHERE ordered_item.`event_id`='{event_id}' " \
            "ORDER BY order_date "
        cursor.execute(sql)
        items = cursor.fetchall()
        # print(items)
        cursor.close()
    subtotal = sum([item['price'] * item['quantity'] for item in items])

    with connection.cursor() as cursor:
        sql = "SELECT * " \
            "FROM perfect_party.item_option WHERE is_deleted = 0"
        cursor.execute(sql)
        options = cursor.fetchall()
        # print(options)
        cursor.close()

    return render_template("onebook.html", onebook=True, result=result, items=items, options=options, subtotal=subtotal)


@pages.route("/postBooking", methods=['POST'])
def get_id():
    args = json.loads(request.values.get("args"))
    booking_id = int(args['Id'])
    return jsonify(booking_id)

@pages.route('/placeOrder', methods=['POST'])
def place_order():
    booking_id = request.args.get('booking_id')
    item_id = request.form['item_id']
    quantity = request.form['quantity']

    order_date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

    with connection.cursor() as cursor:
        sql = "INSERT INTO ordered_item(event_id, item_id, quantity, order_date) " \
            "SELECT event_id, %s, %s, %s " \
            "FROM booking " \
           f"WHERE booking.booking_id={booking_id} "
        cursor.execute(sql, (item_id, quantity, order_date))
        cursor.close()
    connection.commit()

    return redirect(url_for('pages.get_book') + '?booking_id=' + booking_id)

@pages.route("/venue")
def venue():
    return render_template("venue.html", venue=True)


@pages.route("/getVenue")
def get_venues():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `venue` WHERE is_deleted = 0"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

    venue_list = {}
    list_of_venue = []
    for item in result:
        if item['unit_number'] == '':
            obj = {'VenueName': item['venue_name'],
                   'Address': item['street_number'] + ' ' + item['street_name'],
                   'City': item['city'],
                   'Province': item['province'],
                   'Country': item['country'],
                   'PostalCode': item['postal_code'],
                   'Price': float(item['price']),
                   'ID': item['venue_id'],
                   'Street_Number': item['street_number'],
                   'Street_Name': item['street_name'],
                   'Unit_Number': item['unit_number']}
        else:
            obj = {'VenueName': item['venue_name'],
                   'Address': item['unit_number'] + '-' + item['street_number'] + ' ' + item['street_name'],
                   'City': item['city'],
                   'Province': item['province'],
                   'Country': item['country'],
                   'PostalCode': item['postal_code'],
                   'Price': float(item['price']),
                   'ID': item['venue_id'],
                   'Street_Number': item['street_number'],
                   'Street_Name': item['street_name'],
                   'Unit_Number': item['unit_number']}
        list_of_venue.append(obj)
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
        sql = "INSERT INTO `venue`(venue_name, street_number, street_name, unit_number, " \
              "city, province, country, postal_code, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
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
        sql = "UPDATE `venue` SET venue_name = %s, street_number = %s, street_name = %s, " \
              "unit_number = %s, city = %s, province = %s, country = %s, postal_code = %s, price = %d" \
              " WHERE venue_id = %d;" % (repr(name), repr(str_number), repr(str_name), repr(unit_number),
                                         repr(city), repr(province), repr(country), repr(postal), int(price), int(id))
        print(sql)
        cursor.execute(sql)
        connection.commit()
        cursor.close()
    return redirect(url_for('pages.venue'))



@pages.route('/deleteBooking', methods=['GET'])
def delete_booking():
    id = request.args.get('id')

    with connection.cursor() as cursor:
        sql = "UPDATE `booking` SET is_deleted = 1 WHERE booking_id = %d;" % int(id)
        print(sql)
        cursor.execute(sql)
        connection.commit()
        cursor.close()

    return redirect(url_for('pages.booking'))


@pages.route('/deleteVenue', methods=['POST'])
def delete_venue():
    print(request.form)
    id = request.form['id']

    with connection.cursor() as cursor:
        sql = "UPDATE `venue` SET is_deleted = 1 WHERE venue_id = %d;" % int(id)
        print(sql)
        cursor.execute(sql)
        connection.commit()
        cursor.close()

    return redirect(url_for('pages.venue'))


@pages.route("/client")
def client():
    return render_template("client.html", client=True)


@pages.route("/getClient")
def get_client():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `client` WHERE is_deleted = 0"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

    client_list = {}
    list_of_client = []
    for item in result:
        if item['unit_number'] == '' or item['unit_number'] == None:
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
        cursor.close()
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
def delete_client(): \
        # implementation here
    print(request.form)
    id = request.form['id']

    with connection.cursor() as cursor:
        sql = "UPDATE `client` SET is_deleted = 1 WHERE client_id = %d;" % int(id)
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
        sql = "SELECT * FROM `supplier` WHERE is_deleted = 0"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

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
        cursor.close()

    return redirect(url_for('pages.supplier'))


@pages.route('/deleteSupplier', methods=['POST'])
def delete_supplier():
    print(request.form)
    id = request.form['id']

    with connection.cursor() as cursor:
        sql = "UPDATE `supplier` SET is_deleted = 1 WHERE supplier_id = %d;" % int(id)
        print(sql)
        cursor.execute(sql)
        connection.commit()
        cursor.close()

    return redirect(url_for('pages.supplier'))


@pages.route("/item/getitem")
def get_item():
    item = request.args.get('item')
    with connection.cursor() as cursor:
        sql = "SELECT *" \
              "FROM `perfect_party`.`item_option` as item " \
              "LEFT JOIN `perfect_party`.`supplier` as supplier " \
              "ON item.supplier_id = supplier.supplier_id " \
             f"WHERE item.type = '{item}' AND item.is_deleted = 0"
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

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
    item = request.args.get('item')
    name = request.form['name']
    price = request.form['price']
    supplier_id = request.form['supplier_id']

    with connection.cursor() as cursor:
        sql = "INSERT INTO `item_option` (name, price, supplier_id, type) " \
              "VALUES ({0}, {1}, {2}, {3})".format(repr(name), float(price), supplier_id, repr(item))
        # print(sql)
        cursor.execute(sql)
        connection.commit()
        cursor.close()

    return redirect(url_for(f'pages.item_{item.lower()}'))


@pages.route('/editItem', methods=['POST'])
def edit_item():
    # print(request.form)
    item = request.form['item']
    name = request.form['name']
    price = request.form['price']
    supplier_id = request.form['supplier_id']
    id = request.form['id']

    with connection.cursor() as cursor:
        sql = "UPDATE `item_option` SET name = %s, price = %s, supplier_id = %s " \
              "WHERE item_id = %d;" % (repr(name), float(price), repr(supplier_id), int(id))
        print(sql)
        cursor.execute(sql)
        connection.commit()
        cursor.close()

    return redirect(url_for(f'pages.item_{item.lower()}'))


@pages.route('/deleteItem', methods=['POST'])
def delete_item():
    # print(request.form)
    id = request.form['id']
    item = request.form['item']

    with connection.cursor() as cursor:
        sql = "UPDATE `item_option` SET is_deleted = 1 WHERE item_id = %d;" % int(id)
        # print(sql)
        cursor.execute(sql)
        connection.commit()
        cursor.close()

    return redirect(url_for(f'pages.item_{item.lower()}'))


def item(item):
    with connection.cursor() as cursor:
        sql = "SELECT * " \
              "FROM `supplier` " \
             f"WHERE type='{item}' AND is_deleted = 0"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
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


@pages.route("/schema")
def schema():
    with connection.cursor() as cursor:
        sql = "SHOW TABLES"
        cursor.execute(sql)
        tables = cursor.fetchall()
        cursor.close()
    s = []
    for row in tables:
        table = row["Tables_in_perfect_party"]
        with connection.cursor() as cursor:
            sql = f'DESCRIBE `{table}`'
            cursor.execute(sql)
            cols = cursor.fetchall()
        s.append({table: cols})
    return jsonify(s)


@pages.route("/myaccount", methods=['POST', 'GET'])
def myaccount():
    account_id = request.args['account_id']
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `perfect_party`.`account` as account " \
              "WHERE account_id = {0} AND is_deleted = 0".format(account_id)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
    return render_template("myaccount.html", result=result, myaccount=True)


@pages.route("/editAccount", methods=['POST'])
def edit_account():
    result = request.form
    print(request.form)
    return render_template("editaccount.html", result=result)


@pages.route("/updateAccount", methods=['POST'])
def update_account():
    result = request.form
    print(result)
    account_id = result['account_id']

    with connection.cursor() as cursor:
        sql = "UPDATE `perfect_party`.`account` \n" \
              "SET name = {name}, birthday = {birthday}, gender = {gender}, \n" \
              "address = {address}, mobile_phone_number = {mobile}, home_phone_number = {home}, \n" \
              "emergency_contact_name = {ename}, emergency_contact_number = {enumber} \n" \
              "WHERE account_id = {account_id}".format(name=repr(result['name']),
                                                       birthday=repr(result['birthday']),
                                                       gender=repr(result['gender']),
                                                       address=repr(result['address']),
                                                       mobile=repr(result['mobile_phone_number']),
                                                       home=repr(result['home_phone_number']),
                                                       ename=repr(result['emergency_contact_name']),
                                                       enumber=repr(result['emergency_contact_number']),
                                                       account_id=account_id)
        print(sql)
        cursor.execute(sql)
        cursor.close()

    return redirect(url_for("pages.myaccount", account_id=account_id))
