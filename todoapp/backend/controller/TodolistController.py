from flask import Blueprint, jsonify
from todoapp.backend.util import RequestUtils, Response
from todoapp.backend.util.DbConnector import DbConnector
import psycopg2
import datetime
from loguru import logger
from todoapp.backend.server.TodolistServer import encode_auth_token,decode_auth_token
from flask import request

app_info = Blueprint("app_info", __name__)

database = DbConnector()


# @app_info.route("/users", methods=["GET"])
# def get_users():
#     cur = database.getCursor()
#     cur.execute('SELECT * FROM users;')
#     users = cur.fetchall()
#
#     database.close()
#
#     return Response.success(users)


@app_info.route("/users", methods=["POST"])
def register_user():
    # get user input from front-end
    username = RequestUtils.get("username").lower()
    password = RequestUtils.get("password").lower()
    role = RequestUtils.get("role").lower()
    # check the username is unique
    cur = database.getCursor()
    cur.execute('SELECT * FROM users WHERE username=\'' + username + '\';')
    print(cur.rowcount)
    if cur.rowcount != 0:
      database.close()
      return Response.fail()
    else:
      # if the username is unique, insert into database
      insert_query = """INSERT INTO users (username, password, role) VALUES (%s,%s,%s)"""
      insert_data = (username, password, role)

      cur.execute(insert_query, insert_data)
      database.connection.commit()

      data = {
        "username": username,
        "role": role
      }

      database.close()

      return Response.success(data)


@app_info.route("/login", methods=["GET"])
def login():
    # get user input from front-end
    username = RequestUtils.get("username").lower()
    password = RequestUtils.get("password").lower()

    # verify username and password
    cur = database.getCursor()
    cur.execute('SELECT * FROM users WHERE username=\'' + username + '\';')
    user = cur.fetchall()

    user_data = {
      "user_id": user[0][0],
      "username": user[0][1],
      "role": user[0][3]
    }

    # return JWT token
    if user[0][2] == password:
      JWTToken = encode_auth_token(user_data)
      database.close()
      return Response.success(JWTToken)
    else:
      database.close()
      return Response.fail()



@app_info.route("/items", methods=["POST"])
def add_new_item():
    """
      Add operation
      verify user's JWT token and add item to their items_table
    """
    result = decode_auth_token(str(request.headers['Jwttoken']))

    # verify user's login information
    if result[0] == 200:
      user_id = result[1]['user_id']
      item = RequestUtils.get("item").lower()
      try:
          cur = database.getCursor()
          insert_query = """INSERT INTO items_table(user_id, items, create_date) VALUES (%s,%s,%s)"""
          insert_data = (user_id, item, datetime.datetime.now())

          cur.execute(insert_query, insert_data)
          database.connection.commit()
          # count = cur.rowcount
          # print(count, "Record inserted successfully into mobile table")
      except (Exception, psycopg2.Error) as error:
          logger.error(error)
          return Response.fail()
      finally:
          database.close()
          print("PostgreSQL connection is closed")

      return Response.success(item)
    else:
      print(decode_auth_token(str(request.headers['Jwttoken']))[1])
      return Response.fail()


@app_info.route("/items", methods=["PUT"])
def update_item():
  """
  Update Operation
  verify user's JWT token and update the item user choose
  """
  result = decode_auth_token(str(request.headers['Jwttoken']))
  item_id = str(request.headers["item_id"])

  content = RequestUtils.get("item").lower()

  # verify user's login information
  if result[0] == 200:
    user_id = result[1]['user_id']
    try:
      cur = database.getCursor()
      query = """UPDATE items_table set items = %s WHERE user_id = %s AND id = %s"""
      data = (content, user_id, item_id)

      cur.execute(query, data)
      database.connection.commit()
    except (Exception, psycopg2.Error) as error:
      logger.error(error)
      return Response.fail()
    finally:
      database.close()
      print("PostgreSQL connection is closed")

    return Response.success(content)
  else:
    print(decode_auth_token(str(request.headers['Jwttoken']))[1])
    return Response.fail()


@app_info.route("/items", methods=["DELETE"])
def delete_item():
  """
  Delete Operation
  verify user's JWT token and delete the item user choose
  """
  result = decode_auth_token(str(request.headers['Jwttoken']))
  item_id = str(request.headers["item_id"])

  # verify user's login information
  if result[0] == 200:
    user_id = result[1]['user_id']

    try:
      cur = database.getCursor()
      query = """DELETE FROM items_table WHERE user_id = %s AND id = %s"""
      data = (user_id, item_id)

      cur.execute(query, data)
      database.connection.commit()
    except (Exception, psycopg2.Error) as error:
      logger.error(error)
      return Response.fail()
    finally:
      database.close()
      print("PostgreSQL connection is closed")

    return Response.success("this item has been deleted")
  else:
    print(decode_auth_token(str(request.headers['Jwttoken']))[1])
    return Response.fail()


@app_info.route("/items", methods=["GET"])
def get_item_by_user_id():
    #verify JWT token
    result = decode_auth_token(str(request.headers['Jwttoken']))

    if result[0] == 200:

      cur = database.getCursor()
      user_id = result[1]['user_id']
      cur.execute('SELECT * FROM items_table WHERE user_id=\'' + user_id + '\';')
      item = cur.fetchall()
      database.close()
      return Response.success(item)

    else:
      print(decode_auth_token(str(request.headers['Jwttoken']))[1])
      return Response.fail()








