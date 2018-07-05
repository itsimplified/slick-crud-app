# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, redirect, render_template
import pandas as pd
from sqlalchemy import create_engine
import re
import sys
sys.path.insert(1, "/home/ard9476/.local/lib/python2.7/site-packages")
sys.path.insert(2, "/home/ard9476/mysite/")      #needs to add folder for each company


app = Flask(__name__)

@app.route('/')
def run_script():
    url = request.url
    if 'company' in url:
        company = re.search(r'company=(.*?)&myscript', url).group(1)
        myscript = re.search(r'myscript=(.*?)&data', url).group(1)
        data = url.split("data=",1)[1]
    else:
        return 'Welcome to my page!'

    #need to define this for every company page app that gets redirected
    if str(company) == 'cabildo' and str(myscript) == 'upload':
        from cabildo.upload import open     #need to include the init file in folder to import
        output = open(data)                 #runs program
        if output == 'Import successfull!':
            return redirect('http://www.apps-simplified.com/Portals/Cabildo/upload/upload.php?success=1')                      #must return something; even output
        else:
            return redirect('http://www.apps-simplified.com/Portals/Cabildo/upload/upload.php?fail=1')
    if str(company) == 'posts' and str(myscript) == 'mrecommender':
        import ast
        newdata = ast.literal_eval(data)    #convert unicode to dictionary
        from posts.movieRe import rate     #need to include the init file in folder to import
        IP = request.headers['X-Real-IP']
        output = rate(newdata,IP)                 #runs program
        if output == 'Recommendations successfull!':
            return redirect('http://www.itsimplified-ms.com/posts/movie-recommender.php?success=1')                      #must return something; even output
        else:
            return redirect('http://www.itsimplified-ms.com/posts/movie-recommender.php?fail=1')
    if str(company) == 'posts' and str(myscript) == 'spredictor':
        import ast
        newdata = ast.literal_eval(data)    #convert unicode to dictionary
        from posts.semenQual import quality     #need to include the init file in folder to import
        IP = request.headers['X-Real-IP']	#this only works in pythonanywhere to get ip
        output = quality(newdata,IP)                 #runs program
        if output == 'Recommendations successfull!':
            return redirect('http://www.itsimplified-ms.com/posts/semen-predictor.php?success=1')                      #must return something; even output
        else:
            return redirect('http://www.itsimplified-ms.com/posts/semen-predictor.php?fail=1')

@app.route('/SQLdatabase')  #user types this in URL
def sql_database():
    from posts.SQLquery import sql_query
    results = sql_query(''' SELECT * FROM data_table''')
    return render_template('sqldatabase.html', results=results)   #you need to put this in the templates directory
@app.route('/insert',methods = ['POST', 'GET']) #this is when user submits an insert
def sql_datainsert():
    from posts.SQLquery import sql_edit_insert, sql_query
    if request.method == 'POST':
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']
        sql_edit_insert(''' INSERT INTO data_table (first_name,last_name,address,city,state,zip) VALUES (?,?,?,?,?,?) ''', (first_name,last_name,address,city,state,zip) )
    results = sql_query(''' SELECT * FROM data_table''')
    msg = 'INSERT INTO data_table (first_name,last_name,address,city,state,zip) VALUES ('+first_name+','+last_name+','+address+','+city+','+state+','+zip+')'
    return render_template('sqldatabase.html', results=results, msg=msg)   #you need to put this in the templates directory
@app.route('/delete',methods = ['POST', 'GET']) #this is when user clicks delete link
def sql_datadelete():
    from posts.SQLquery import sql_delete, sql_query
    if request.method == 'GET':
        lname = request.args.get('lname')
        fname = request.args.get('fname')
        sql_delete(''' DELETE FROM data_table where first_name = ? and last_name = ?''', (fname,lname) )
    results = sql_query(''' SELECT * FROM data_table''')
    msg = 'DELETE FROM data_table WHERE first_name = ' + fname + ' and last_name = ' + lname
    return render_template('sqldatabase.html', results=results, msg=msg)
@app.route('/query_edit',methods = ['POST', 'GET']) #this is when user clicks edit link
def sql_editlink():
    from posts.SQLquery import sql_query, sql_query2
    if request.method == 'GET':
        elname = request.args.get('elname')
        efname = request.args.get('efname')
        eresults = sql_query2(''' SELECT * FROM data_table where first_name = ? and last_name = ?''', (efname,elname))
    results = sql_query(''' SELECT * FROM data_table''')
    return render_template('sqldatabase.html', eresults=eresults, results=results)
@app.route('/edit',methods = ['POST', 'GET']) #this is when user submits an edit
def sql_dataedit():
    from posts.SQLquery import sql_edit_insert, sql_query
    if request.method == 'POST':
        old_last_name = request.form['old_last_name']
        old_first_name = request.form['old_first_name']
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']
        sql_edit_insert(''' UPDATE data_table set first_name=?,last_name=?,address=?,city=?,state=?,zip=? WHERE first_name=? and last_name=? ''', (first_name,last_name,address,city,state,zip,old_first_name,old_last_name) )
    results = sql_query(''' SELECT * FROM data_table''')
    msg = 'UPDATE data_table set first_name = ' + first_name + ', last_name = ' + last_name + ', address = ' + address + ', city = ' + city + ', state = ' + state + ', zip = ' + zip + ' WHERE first_name = ' + old_first_name + ' and last_name = ' + old_last_name
    return render_template('sqldatabase.html', results=results, msg=msg)

