# prediction function
import os
from flask_mysqldb import MySQL
import mysql.connector
import numpy as np
from flask import Flask,render_template,request,url_for
from jinja2 import FileSystemLoader
import pandas as pd
import matplotlib
matplotlib.use('agg')
from flask_bootstrap import Bootstrap

import matplotlib.pyplot as plt
import io
import base64


app=Flask(__name__)
bootstrap = Bootstrap(app)
app.config['STATIC_FOLDER'] = 'static'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Nandini@0608'
app.config['MYSQL_DB'] = 'big_alley'
mysql = MySQL(app)


@app.route('/')

def index():
    return render_template('index copy.html')

@app.route('/agent_office')


def  agent_office():
    return render_template('agent_office.html')

@app.route('/agent')
def  agent():
    return render_template('login.html')

@app.route('/handle_agent', methods=['POST'])
def handle_agent():
    Name = request.form.get('Name')
    password = request.form.get('password')
    print(Name)
    
    if password is not None:
        password = int(password)
    else:
        return " entry"
        
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM agent where agent_id={} and name='{}'".format(password, Name))

    results = cur.fetchall()
    if len(results) > 0:
        cur.execute("Select * from available where agent_id={}".format(password))
        column_names = [desc[0] for desc in cur.description]
        re=cur.fetchall()
        return render_template('agent.html',data=re,column_names=column_names)
    else:
        return render_template('login.html')

@app.route('/rent_forms', methods=['POST'])
def rent_forms():
    name=request.form.get('name')
    house_no=int(request.form.get('house_no'))
    street_name=request.form.get('street_name')
    year_of_rent=int(request.form.get('year_of_rent'))
    tenant=request.form.get('tenant')
    agent_id=int(request.form.get('agent_id'))
    print('hello')
    cur = mysql.connection.cursor()
    print(name)
    print(house_no)
    print(street_name)
    try:
        cur.execute("update available set status='rented' where agent_id={} and house_no={} and street='{}'".format(agent_id, house_no, street_name))
        cur.execute("update  rent set rented_to='{}' where house_no={} and street='{}'".format(tenant,house_no,street_name))
        cur.execute("update  rent set year_of_rent={} where house_no={} and street='{}' ".format(year_of_rent,house_no,street_name))
        mysql.connection.commit()
        cur.close()
        return render_template('last.html',agent_id=agent_id,name=name)
    except Exception as e:
        print(e)
        return render_template('login.html')
    
@app.route('/sell_forms', methods=['POST'])
def sell_forms():
    name=request.form.get('name')
    house_no=int(request.form.get('house_no'))
    street_name=request.form.get('street_name')
    year_of_sale=int(request.form.get('year_of_sale'))
    new=request.form.get('new')
    agent_id=int(request.form.get('agent_id'))
    print('hello')
    cur = mysql.connection.cursor()
    print(name)
    print(house_no)
    print(street_name)
    try:
        cur.execute("update available set status='sold' where agent_id={} and house_no={} and street='{}'".format(agent_id, house_no, street_name))
        cur.execute("update  house set owner ='{}' where house_no={} and street='{}'".format(new,house_no,street_name))
        cur.execute("update  sold set year_of_sale={} where house_no={} and street='{}' ".format(year_of_sale,house_no,street_name))
        mysql.connection.commit()
        cur.close()
        return render_template('last.html',agent_id=agent_id,name=name)
    except Exception as e:
        print(e)
        return render_template('login.html')
    
@app.route('/redirect',methods=['POST','GET'])
def redirect():
    cur = mysql.connection.cursor()
    name = request.args.get('name')
    agent_id = request.args.get('agent_id')
    print(name)
    print(type(agent_id))
    print(agent_id)
    cur.execute("SELECT * FROM agent where agent_id=%s and name=%s", (agent_id, name))

    results = cur.fetchall()
    if len(results) > 0:
        cur.execute("Select * from available where agent_id={}".format(agent_id))
        re=cur.fetchall()
        return render_template('agent.html',data=re)
    else:
        return render_template('login.html')

    


@app.route('/admin')
def  admin():
    #os.system('start cmd')
    os.system('x-terminal-emulator')
    return render_template('index copy.html')

@app.route('/reports_auth')
def reports_auth():
    return render_template('reports_auth.html')

@app.route('/listings')
def listings():
    return render_template('listings.html')

@app.route('/fetch_tables',methods=['POST'])
def fetch_tables():
    cur = mysql.connection.cursor()
    table_name = request.form.get('table')
    cur.execute("SELECT * FROM {}".format(table_name))
    column_names = [desc[0] for desc in cur.description]
    results = cur.fetchall()
    cur.close()
    return render_template('table.html',data=results,column_names=column_names)

@app.route('/rent',methods=['POST'])
def sales():
    cur = mysql.connection.cursor()
    cur.execute("select * from rent natural join agent natural join available")
    results = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    cur.close()
    return render_template('table.html',data=results,column_names=column_names)

@app.route('/sales_rent', methods=['POST','GET'])
def sales_rent():
    # establish connection to the database
    cur = mysql.connection.cursor()

    # get id from form data
    id = request.form.get('id')

    # execute SQL queries to retrieve sales and rent data for the given agent id
    cur.execute("select sold.house_no,sold.street,sold.agent_id,sold.year_of_sale,agent.name,house.landmark,house.pincode,house.size,house.year_of_cons,available.price from sold natural join agent natural join house natural join available where agent.agent_id={};".format(id))
    results = cur.fetchall()
    cur.execute("select rent.house_no,rent.street,rent.agent_id,rent.year_of_rent,agent.name,house.landmark,house.pincode,house.size,house.year_of_cons,available.price from rent natural join agent natural join house natural join available where agent.agent_id={};".format(id))
    results1 = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]

    # combine sales and rent data into a single list
    data = results + results1

    try:
        # execute SQL query to retrieve revenue data for the given agent id and plot a line chart
        cur.execute("with year as(select year_of_rent from rent union select year_of_sale from sold) select year.year_of_rent, get_total({}, year_of_rent) from year order by year_of_rent".format(id))
        result = cur.fetchall()
        x_values = [result[0] for result in result]
        y_values = [result[1] for result in result]

        # create a new figure and axis object for the plot
        fig, ax = plt.subplots()
        ax.plot(x_values, y_values)
        ax.set_ylabel('Revenue in that year')
        ax.set_xlabel('Year')
        ax.set_title('Performance of Agent '+str(id))
        plt.savefig('static/sales_rent.png')

    except Exception as e:
        print(f"An exception occurred: {e}")

    # render the template with the data and the generated chart
    return render_template('table_rent_sale.html', data=data,column_names=column_names)

@app.route('/plot', methods=['POST','GET'])
def plot():
    try:
        cur = mysql.connection.cursor()
        cur.execute("select agent_id as id, sum(price) as sum from available group by agent_id")
        data = cur.fetchall()
        x_values = [result[0] for result in data]
        y_values = [result[1] for result in data]

        # create a new figure and axis object for the plot
        fig, ax = plt.subplots()
        ax.bar(x_values, y_values)
        ax.set_ylabel('Revenue')
        ax.set_xlabel('Agent')
        ax.set_title('Performance of Agents (Overall)')
        plt.savefig('static/performance.png')

        # Return an HTML page that displays the plot as an image
        return render_template("performance.html")

    except Exception as e:
        print(f"An exception occurred: {e}")



if __name__=="__main__":
    app.run()