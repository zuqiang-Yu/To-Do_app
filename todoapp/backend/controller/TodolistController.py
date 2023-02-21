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
  engine = database.connect_with_connector()
  rowcount = engine.execute("""SELECT * FROM users_table WHERE username= %s;""", (username)).rowcount

  if rowcount != 0:
    return Response.fail()
  else:
    # if the username is unique, insert into database
    insert_query = """INSERT INTO users_table (username, password, admin) VALUES (%s,%s,%s)"""
    insert_data = (username, password, admin)

    engine.execute(insert_query, insert_data)

    return Response.success()

@app_info.route("/login", methods=["POST"])
def login():
  """
  Login interface
  verify user's username and password, if correct return encode jwt token
  """
  # get user input from front-end
  username = RequestUtils.get("username")
  password = RequestUtils.get("password")

  # verify username and password
  engine = database.connect_with_connector()
  user = engine.execute("""SELECT * FROM users_table WHERE username= %s;""", (username)).fetchall()


  user_data = {
    "user_id": str(user[0][0]),
    "username": user[0][1],
    "admin": user[0][3]
  }

  # return JWT token
  if user[0][2] == password:
    JWTToken = encode_auth_token(user_data)
    return Response.success(JWTToken)
  else:
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
        # insert item into items_table
        engine = database.connect_with_connector()
        insert_query = """INSERT INTO items_table(user_id, items, create_date) VALUES (%s,%s,%s) RETURNING id;"""
        insert_data = (user_id, item, datetime.datetime.now())
        item_id = engine.execute(insert_query, insert_data).fetchone()[0]
        # insert user's operation into items_log_table
        insert_query = """INSERT INTO items_log_table(item_id,user_id,items,operation_type,operation_date) VALUES (%s,%s,%s,%s,%s);"""
        insert_data = (item_id, user_id, item, 'add', datetime.datetime.now())
        engine.execute(insert_query, insert_data)

      except (Exception, psycopg2.Error) as error:
          logger.error(error)
          return Response.fail()

      return Response.success("Item has been added into database: " + item)
    else:
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

    try:
      # update item's content
      engine = database.connect_with_connector()
      query = """UPDATE items_table set items = %s WHERE user_id = %s AND id = %s;"""
      data = (content, user_id, item_id)
      engine.execute(query, data)


      # insert user's operation into items_log_table
      query = """INSERT INTO items_log_table(item_id,user_id,items,operation_type,operation_date) VALUES (%s,%s,%s,%s,%s);"""
      data = (item_id, user_id, content, 'update', datetime.datetime.now())

      engine.execute(query, data)

    except (Exception, psycopg2.Error) as error:
      logger.error(error)
      return Response.fail()

    return Response.success(content)
  else:
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
      # update items_table
      engine = database.connect_with_connector()
      query = """DELETE FROM items_table WHERE user_id = %s AND id = %s;"""
      data = (user_id, item_id)
      engine.execute(query, data)

      # insert user's operation into items_log_table
      query = """INSERT INTO items_log_table(item_id,user_id,items,operation_type,operation_date) VALUES (%s,%s,%s,%s,%s);"""
      data = (item_id, user_id, '', 'delete', datetime.datetime.now())
      engine.execute(query, data)

    except (Exception, psycopg2.Error) as error:
      logger.error(error)
      return Response.fail()

    return Response.success("this item has been deleted")

  else:
    return Response.fail()

@app_info.route("/user_items", methods=["GET"])
def get_item_by_user_id():
  """
  GET items list
  get all items from items_table by user_id
  """
  #verify JWT token
  result = decode_auth_token(str(request.headers['Jwttoken']))

  if result[0] == 200:

    engine = database.connect_with_connector()
    user_id = result[1]['user_id']
    items = engine.execute("""SELECT * FROM items_table WHERE user_id = %s;""", (user_id)).fetchall()

    # convert data type
    data = []
    if len(items) > 0:
      for i in range(len(items)):
        item = {
          "id": str(items[i][0]),
          "item": items[i][2],
          "create_date": items[i][3]

        }
        data.append(item)

    return Response.success(data)

  else:
    return Response.fail()

@app_info.route("/sys_user/get_all", methods=["GET"])
def get_all_users_item():
  """
    Get items list
    verify user's JWT token and role
  """
  result = decode_auth_token(str(request.headers['Jwttoken']))


  # verify user's login information
  if result[0] == 200 and result[1]['admin'] == True:

    try:
      engine = database.connect_with_connector()
      query = """SELECT * FROM items_log_table;"""

      logs = engine.execute(query).fetchall()

      # convert data type
      data = []
      if len(logs) > 0:
        for i in range(len(logs)):
          item = {
            "id": str(logs[i][0]),
            "item_id": str(logs[i][1]),
            "user_id": str(logs[i][2]),
            "item": logs[i][3],
            "operation_type": logs[i][4],
            "operation_date": logs[i][5]

          }
          data.append(item)



    except (Exception, psycopg2.Error) as error:
      logger.error(error)
      return Response.fail()


    return Response.success(data)
  else:
    return Response.fail()







