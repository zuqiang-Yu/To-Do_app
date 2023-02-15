from flask import Blueprint, jsonify
from todoapp.backend.util import RequestUtils, Response
from todoapp.backend.util.DbConnector import DbConnector
import psycopg2
import datetime
from loguru import logger

app_info = Blueprint("app_info", __name__)

database = DbConnector()


@app_info.route("/users", methods=["GET"])
def get_users():
    cur = database.getCursor()
    cur.execute('SELECT * FROM users;')
    users = cur.fetchall()

    database.close()

    return Response.success(users)


@app_info.route("/users", methods=["POST"])
def register_user():
    username = RequestUtils.get("username").lower()
    password = RequestUtils.get("password").lower()
    role = RequestUtils.get("role").lower()

    cur = database.getCursor()
    insert_query = """INSERT INTO users (username, password, role) VALUES (%s,%s,%s)"""
    insert_data = (username, password, role)

    cur.execute(insert_query, insert_data)
    database.connection.commit()
    count = cur.rowcount
    print(count, "Record inserted successfully into mobile table")

    database.close()

    return Response.success(count)


@app_info.route("/items", methods=["POST"])
def add_new_item():
    user_id = RequestUtils.get("user_id").lower()
    item = RequestUtils.get("item").lower()
    try:
        cur = database.getCursor()
        insert_query = """INSERT INTO items_table(user_id, items, create_date) VALUES (%s,%s,%s)"""
        insert_data = (user_id, item, datetime.datetime.now())

        cur.execute(insert_query, insert_data)
        database.connection.commit()
        count = cur.rowcount
        print(count, "Record inserted successfully into mobile table")
    except (Exception, psycopg2.Error) as error:
        logger.error(error)
        return Response.fail()
    finally:
        database.close()
        print("PostgreSQL connection is closed")

    return Response.success(count)


@app_info.route("/items", methods=["GET"])
def get_item_by_user_id():
    cur = database.getCursor()
    user_id = RequestUtils.get("user_id").lower()
    cur.execute('SELECT * FROM items_table WHERE user_id=\'' + user_id + '\';')
    item = cur.fetchall()

    database.close()

    return Response.success(item)
