# main.py
import os
import base64
import io
import math
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import mysql.connector
import hashlib
import datetime
import calendar
import random
from random import randint
from urllib.request import urlopen
import webbrowser

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from werkzeug.utils import secure_filename
from PIL import Image

import urllib.request
import urllib.parse


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="mendman"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""

  
    return render_template('index.html',msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""
    act=request.args.get("act")

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM customer WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('userhome'))
        else:
            msg = 'Incorrect username/password! or access not provided'
    return render_template('login.html',msg=msg,act=act)

@app.route('/login_pro', methods=['GET', 'POST'])
def login_pro():
    msg=""
    act=request.args.get("act")
    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM service_provider WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('sp_home'))
        else:
            msg = 'Incorrect username/password! or access not provided'
    return render_template('login_pro.html',msg=msg,act=act)

@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password! or access not provided'
    return render_template('login_admin.html',msg=msg)




@app.route('/register', methods=['GET', 'POST'])
def register():
    
    msg=""
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    if request.method=='POST':
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['address']
        city=request.form['city']
        uname=request.form['uname']
        pass1=request.form['pass']
      
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM customer where uname=%s",(uname,))
        cnt = mycursor.fetchone()[0]

        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM customer")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
                    
            sql = "INSERT INTO customer(id,name,mobile,email,address,city,uname,pass,rdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid,name,mobile,email,address,city,uname,pass1,rdate)
            mycursor.execute(sql, val)
            mydb.commit()            
            #print(mycursor.rowcount, "Registered Success")
            msg="sucess"
            #if mycursor.rowcount==1:
            return redirect(url_for('login',act='1'))
        else:
            msg='Already Exist'
    return render_template('register.html',msg=msg)

@app.route('/reg_sp', methods=['GET', 'POST'])
def reg_sp():
    
    msg=""
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")

    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM services')
    sdata = cursor.fetchall()

    
    if request.method=='POST':
        name=request.form['name']
        service_name=request.form['service_name']
        mobile=request.form['mobile']
        email=request.form['email']
        location=request.form['location']
        city=request.form['city']
        uname=request.form['uname']
        pass1=request.form['pass']
      
        
        cursor.execute("SELECT count(*) FROM service_provider where uname=%s",(uname,))
        cnt = cursor.fetchone()[0]

        if cnt==0:
            cursor.execute("SELECT max(id)+1 FROM service_provider")
            maxid = cursor.fetchone()[0]
            if maxid is None:
                maxid=1
                    
            sql = "INSERT INTO service_provider(id,name,service_name,mobile,email,location,city,uname,pass,rdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid,name,service_name,mobile,email,location,city,uname,pass1,rdate)
            cursor.execute(sql, val)
            mydb.commit()            
            #print(mycursor.rowcount, "Registered Success")
            msg="sucess"
            #if mycursor.rowcount==1:
            return redirect(url_for('login_pro',act='1'))
        else:
            msg='Already Exist'
    return render_template('reg_sp.html',msg=msg,sdata=sdata)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    act=request.args.get('act')
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM services')
    data = cursor.fetchall()

    if request.method=='POST':
        sname=request.form['sname']
        cursor.execute("SELECT max(id)+1 FROM services")
        maxid = cursor.fetchone()[0]
        if maxid is None:
            maxid=1
                
        sql = "INSERT INTO services(id,service_name) VALUES (%s, %s)"
        val = (maxid,sname)
        cursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('admin',act='1'))
            
    if act=="del":
        did=request.args.get("did")
        cursor.execute("delete from services where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('admin'))
    return render_template('admin.html',msg=msg,data=data,act=act)


@app.route('/view_sp', methods=['GET', 'POST'])
def view_sp():
    msg=""
    act=request.args.get('act')
    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM services')
    sdata = cursor.fetchall()
    
    cursor.execute('SELECT * FROM service_provider')
    data = cursor.fetchall()

    if request.method=='POST':
        sname=request.form['sname']
        if sname=="All":
            print("")
        else:
            cursor.execute('SELECT * FROM service_provider where service_name=%s',(sname,))
            data = cursor.fetchall()

    if act=="ok":
        sid=request.args.get("sid")
        cursor.execute("update service_provider set status=1 where id=%s",(sid,))
        mydb.commit()
        return redirect(url_for('view_sp'))
    
    if act=="del":
        did=request.args.get("did")
        cursor.execute("delete from service_provider where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_sp'))     

    return render_template('view_sp.html',msg=msg,act=act,sdata=sdata,data=data)





@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""
    cnt=0
    uname=""
    act = request.args.get('act')
    cat = request.args.get('cat')
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM customer where uname=%s",(uname,))
    usr = mycursor.fetchone()

    mycursor.execute("SELECT distinct(service_name) from service_provider")
    data2 = mycursor.fetchall()


    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    
    return render_template('userhome.html',msg=msg,data2=data2,usr=usr)

#SVM Classification
class SVM:
    def fit(self, X, y):
        n_samples, n_features = X.shape# P = X^T X
        K = np.zeros((n_samples, n_samples))
        for i in range(n_samples):
            for j in range(n_samples):
                K[i,j] = np.dot(X[i], X[j])
                P = cvxopt.matrix(np.outer(y, y) * K)# q = -1 (1xN)
        q = cvxopt.matrix(np.ones(n_samples) * -1)# A = y^T 
        A = cvxopt.matrix(y, (1, n_samples))# b = 0 
        b = cvxopt.matrix(0.0)# -1 (NxN)
        G = cvxopt.matrix(np.diag(np.ones(n_samples) * -1))# 0 (1xN)
        h = cvxopt.matrix(np.zeros(n_samples))
        solution = cvxopt.solvers.qp(P, q, G, h, A, b)# Lagrange multipliers
        a = np.ravel(solution['x'])# Lagrange have non zero lagrange multipliers
        sv = a > 1e-5
        ind = np.arange(len(a))[sv]
        self.a = a[sv]
        self.sv = X[sv]
        self.sv_y = y[sv]# Intercept
        self.b = 0
        for n in range(len(self.a)):
            self.b += self.sv_y[n]
            self.b -= np.sum(self.a * self.sv_y * K[ind[n], sv])
        self.b /= len(self.a)# Weights
        self.w = np.zeros(n_features)
        for n in range(len(self.a)):
            self.w += self.a[n] * self.sv_y[n] * self.sv[n]
        
    def project(self, X):
        return np.dot(X, self.w) + self.b
    
    
    def predict(self, X):
        return np.sign(self.project(X))
@app.route('/user_sp', methods=['GET', 'POST'])
def user_sp():
    msg=""
    cnt=0
    uname=""
    sp = request.args.get('sp')
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM customer where uname=%s",(uname,))
    usr = mycursor.fetchone()
   

    mycursor.execute("SELECT * from service_provider where service_name=%s && available_st=0",(sp,))
    data2 = mycursor.fetchall()


    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")

    if request.method=='POST':
        loc=request.form['loc']
        vv='%'+loc+'%'
        mycursor.execute("SELECT * from service_provider where (service_name=%s && available_st=0) && (location like %s || city like %s)",(sp,vv,vv))
        data2 = mycursor.fetchall()
        
        
    
    
    return render_template('user_sp.html',msg=msg,data2=data2,usr=usr,sp=sp)



@app.route('/user_book', methods=['GET', 'POST'])
def user_book():
    msg=""
    cnt=0
    uname=""
    st=""
    sname = request.args.get('sname')
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM customer where uname=%s",(uname,))
    usr = mycursor.fetchone()
   

    mycursor.execute("SELECT * from service_provider where uname=%s",(sname,))
    data2 = mycursor.fetchone()
    name=data2[1]
    mobile=data2[3]
    service=data2[2]


    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")

    if request.method=='POST':
        sdate=request.form['sdate']
        stime=request.form['stime']

        mycursor.execute("SELECT max(id)+1 FROM service_booking")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        sql = "INSERT INTO service_booking(id, uname, sname, service, sdate, stime, rdate, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid, uname, sname, service, sdate, stime, rdate, '0')
        mycursor.execute(sql,val)
        mydb.commit()

        mess=service+" Booked by "+uname
        url="http://iotcloud.co.in/testsms/sms.php?sms=msg&name="+name+"&mess="+mess+"&mobile="+str(mobile)
        webbrowser.open_new(url)
        
        st="1"
        msg="Booked Success"
            
    
    
    return render_template('user_book.html',msg=msg,data2=data2,usr=usr,st=st)


@app.route('/book', methods=['GET', 'POST'])
def book():
    msg=""
    cnt=0
    uname=""
    sp = request.args.get('sp')
    act = request.args.get('act')
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM customer where uname=%s",(uname,))
    usr = mycursor.fetchone()
   

    mycursor.execute("SELECT * from service_booking where uname=%s",(uname,))
    data2 = mycursor.fetchall()


    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")

    if act=="ok":
        rid=request.args.get("rid")
        sname=request.args.get("sname")
        mycursor.execute("update service_booking set status=2 where id=%s",(rid,))
        mydb.commit()

        mycursor.execute("update service_provider set available_st=0 where uname=%s",(sname,))
        mydb.commit()
        
        return redirect(url_for('book'))
    
    return render_template('book.html',msg=msg,data2=data2,usr=usr,sp=sp,act=act)


@app.route('/sp_home', methods=['GET', 'POST'])
def sp_home():
    msg=""
    cnt=0
    uname=""
    act = request.args.get('act')
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM service_provider where uname=%s",(uname,))
    usr = mycursor.fetchone()
   

    mycursor.execute("SELECT * from service_booking s,customer c where s.sname=%s && s.uname=c.uname",(uname,))
    data2 = mycursor.fetchall()


    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    if act=="start":
        rid=request.args.get("rid")
        mycursor.execute("update service_booking set status=1 where id=%s",(rid,))
        mydb.commit()

        mycursor.execute("update service_provider set available_st=1 where uname=%s",(uname,))
        mydb.commit()
        
        return redirect(url_for('sp_home'))
        
    return render_template('sp_home.html',msg=msg,data2=data2,usr=usr,act=act)



@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    msg=""
    act=""
    st=request.args.get('st')
    uname=""
    sname = request.args.get('sname')
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM customer where uname=%s",(uname,))
    usr = mycursor.fetchone()
    email=usr[3]
    name=usr[1]

  

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
   

    if request.method=='POST':
        review=request.form['review']
        
        mycursor.execute("SELECT max(id)+1 FROM service_review")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
            
        sql = "INSERT INTO service_review(id,uname,sname,review,rdate) VALUES (%s, %s, %s, %s, %s)"
        val = (maxid,uname,sname,review,rdate)
        mycursor.execute(sql,val)
        mydb.commit()
        st="1"
        
            
        return redirect(url_for('add_review',st=st))
        

    return render_template('add_review.html',msg=msg,usr=usr,act=act,sname=sname,st=st)



@app.route('/review', methods=['GET', 'POST'])
def review():
    msg=""
    act=""
    sname=request.args.get('sname')
    uname=""
    
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM customer where uname=%s",(uname,))
    usr = mycursor.fetchone()
    email=usr[3]
    name=usr[1]

    mycursor.execute("SELECT * FROM service_review where sname=%s",(sname,))
    data = mycursor.fetchall()
        

    return render_template('review.html',msg=msg,usr=usr,act=act,data=data,sname=sname)




##########################
@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


