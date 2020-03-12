import json
import psycopg2
import os
import collections
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Initialize app
app = Flask(__name__)

# Pull from env
load_dotenv() 

# # Configure db connection
con = psycopg2.connect(database= os.getenv("database_name"), host= os.getenv("host_name"), port= os.getenv("port_number"), user =os.getenv("username"), password = os.getenv("user_password"))
cur = con.cursor()


@app.route('/', methods=['GET'])
def display_data():
    cur.execute("Select * from sales limit 10;")
    rows = cur.fetchall()
    return sql_to_json(rows)

# Transforms rows returned from SQL query to json
def sql_to_json(rows):
    objects_list = []
    for row in rows:
        info_by_column = collections.OrderedDict()
        info_by_column['id'] = row[0]
        info_by_column['firstname'] = row[1]
        info_by_column['lastname'] = row[2]
        info_by_column['productid'] = row[3]
        info_by_column['price'] = row[4]
        info_by_column['saledate'] = row[5]
        objects_list.append(info_by_column)
    converted_json = json.dumps(objects_list, default=str)
    return converted_json


if __name__ == '__main__':
    app.debug = os.environ.get("DEBUG_MODE")
    app.run()
