from flask import Blueprint, jsonify
from todoapp.backend.util import RequestUtils, Response
from todoapp.backend.util.DbConnector import DbConnector
import psycopg2
import datetime
from loguru import logger
from todoapp.backend.server.TodolistServer import encode_auth_token, decode_auth_token
from flask import request

app_info = Blueprint("app_info", __name__)

database = DbConnector()


@app_info.route("/register", methods=["POST"])
def register_user():
  """
  Register interface
  insert new user 's information into database
  """

  # get user input from front-end
  username = RequestUtils.get("username")
  password = RequestUtils.get("password")
  admin = RequestUtils.get("admin")

  # check the username is unique
  cur = database.getCursor()
  cur.execute('SELECT * FROM users_table WHERE username=\'' + username + '\';')
  print(cur.rowcount)

  if cur.rowcount != 0:
    database.close()
    return Response.fail()
  else:
    # if the username is unique, insert into database
    insert_query = """INSERT INTO users_table (username, password, admin) VALUES (%s,%s,%s)"""
    insert_data = (username, password, admin)

    cur.execute(insert_query, insert_data)

    # get row id
    cur.execute('SELECT * FROM users_table WHERE username=\'' + username + '\';')
    last_row_id = cur.fetchall()[0][0]

    database.connection.commit()



    data = {
      "user_id": last_row_id,
      "username": username,
      "admin": admin
    }

    database.close()

    return Response.success(data)

@app_info.route("/login", methods=["GET"])
def login():
  """
  Login interface
  verify user's username and password, if correct return encode jwt token
  """
  # get user input from front-end
  username = RequestUtils.get("username")
  password = RequestUtils.get("password")

  # verify username and password
  cur = database.getCursor()
  cur.execute('SELECT * FROM users_table WHERE username=\'' + username + '\';')
  user = cur.fetchall()

  user_data = {
    "user_id": user[0][0],
    "username": user[0][1],
    "admin": user[0][3]
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
    verifyInfo = decode_auth_token(str(request.headers['Jwttoken']))

    # verify user's login information
    if verifyInfo[0] == 200:
      user_id = verifyInfo[1]['user_id']
      item = RequestUtils.get("item")
      try:
          cur = database.getCursor()
          insert_query = """INSERT INTO items_table(user_id, items, create_date) VALUES (%s,%s,%s) RETURNING id;"""
          insert_data = (user_id, item, datetime.datetime.now())
          cur.execute(insert_query, insert_data)
          item_id = cur.fetchone()[0]
          database.connection.commit()
      except (Exception, psycopg2.Error) as error:
          logger.error(error)
          return Response.fail()

      try:
        insert_query = """INSERT INTO items_log_table(item_id,user_id,items,operation_type,operation_date) VALUES (%s,%s,%s,%s,%s);"""
        insert_data = (item_id,user_id,item,'add',datetime.datetime.now())
        cur.execute(insert_query,insert_data)
        database.connection.commit()
      except (Exception, psycopg2.Error) as error:
        logger.error(error)
        return Response.fail()


      database.close()

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

  content = RequestUtils.get("item")

  # verify user's login information
  if result[0] == 200:
    user_id = result[1]['user_id']
    # update item's content
    try:
      cur = database.getCursor()
      query = """UPDATE items_table set items = %s WHERE user_id = %s AND id = %s;"""
      data = (content, user_id, item_id)

      cur.execute(query, data)
      database.connection.commit()
    except (Exception, psycopg2.Error) as error:
      logger.error(error)
      return Response.fail()

    # insert into items_log_table
    try:
      cur = database.getCursor()
      query = """INSERT INTO items_log_table(item_id,user_id,items,operation_type,operation_date) VALUES (%s,%s,%s,%s,%s);"""
      data = (item_id,user_id,content,'update',datetime.datetime.now())

      cur.execute(query, data)
      database.connection.commit()
    except (Exception, psycopg2.Error) as error:
      logger.error(error)
      return Response.fail()



    database.close()

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
    # update items_table
    try:

      cur = database.getCursor()
      query = """DELETE FROM items_table WHERE user_id = %s AND id = %s;"""
      data = (user_id, item_id)

      cur.execute(query, data)
      database.connection.commit()
    except (Exception, psycopg2.Error) as error:
      logger.error(error)
      return Response.fail()

    # insert into items_log_table
    try:
      cur = database.getCursor()
      query = """INSERT INTO items_log_table(item_id,user_id,items,operation_type,operation_date) VALUES (%s,%s,%s,%s,%s);"""
      data = (item_id, user_id, '', 'delete', datetime.datetime.now())

      cur.execute(query, data)
      database.connection.commit()
    except (Exception, psycopg2.Error) as error:
      logger.error(error)
      return Response.fail()

    database.close()
    return Response.success("this item has been deleted")

  else:
    print(decode_auth_token(str(request.headers['Jwttoken']))[1])
    return Response.fail()


@app_info.route("/items", methods=["GET"])
def get_item_by_user_id():
  """
  GET items list
  get all items from items_table by user_id
  """
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

@app_info.route("/sys_user", methods=["GET"])
def get_all_users_item():
  """
    Get items list
    verify user's JWT token and role
  """
  result = decode_auth_token(str(request.headers['Jwttoken']))


  # verify user's login information
  if result[0] == 200 and result[1]['admin'] == True:

    try:
      cur = database.getCursor()
      query = """SELECT * FROM items_log_table;"""

      cur.execute(query)
      res = cur.fetchall()
      database.connection.commit()
    except (Exception, psycopg2.Error) as error:
      logger.error(error)
      return Response.fail()
    finally:
      database.close()

    return Response.success(res)
  else:
    print(decode_auth_token(str(request.headers['Jwttoken']))[1])
    return Response.fail()







