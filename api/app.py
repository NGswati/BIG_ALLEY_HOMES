# prediction function
from flask_mysqldb import MySQL
import mysql.connector
import numpy as np
from flask import Flask,render_template,request
import re
import requests
import pickle
import requests_html
from jinja2 import FileSystemLoader


app=Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Nandini@0608'
app.config['MYSQL_DB'] = 'test'
mysql = MySQL(app)


@app.route('/')
def hello_world():
    return render_template('initial.html')

@app.route('/show/agent',methods=['POST'])
def agent():
    return render_template('agent.html')

@app.route('/show/office',methods=['POST'])
def office():
    return render_template('office.html')


@app.route('/show',methods=['POST'])
def predict_salary():
    # table=(request.form.get('table'))
    cur = mysql.connection.cursor()
    table_name = request.form.get('table')
    cur.execute("SELECT * FROM {}".format(table_name))

    results = cur.fetchall()
    cur.close()
    return render_template('final.html',data=results)




if __name__=="__main__":
    app.run()