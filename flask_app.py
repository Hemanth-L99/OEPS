from flask import Flask, render_template, flash,request, redirect, url_for, make_response, jsonify, json,jsonify, session
from flask import make_response, request, current_app, redirect, url_for, send_from_directory, g
import os,time,datetime
import  random
import sqlite3 as sql
import json

app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/')
def indexs():
   return render_template('main.html')

@app.route('/login')
def login():
	return render_template('page-login.html')

@app.route('/home')
def home():
	return render_template('main.html')

@app.route('/forget')
def forget():
	return render_template('pages-forget.html')

@app.route('/signup')
def signup():
	return render_template('register.html')

@app.route('/logout')
def logout():
   session.pop('user')
   return render_template('main.html')

# retrieve from table usng row_factory
# sql queries seleted data retreival
# retrieve result from database
@app.route('/dashboard')
def dash():
  return render_template('Dashboard.html')

@app.route('/test2')
def pages():
   return render_template('test2.html')

@app.route('/test3')
def pages1():
   return render_template('test3.html')

@app.route('/test4')
def pages2():
   return render_template('test4.html')
 
@app.route('/test1')
def pages3():
   return render_template('test1.html')

@app.route('/result')
def check():
  if g.user:
    con = sql.connect('main.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from result where username=? ORDER BY timestamps DESC",(g.user,))
    rows = cur.fetchall();
    return render_template('result.html', username=g.user, rows=rows)

#...................register page..............
@app.before_request
def before_request():
  g.user=None
  if 'user' in session:
    g.user=session['user']

@app.route('/addrec', methods=['GET','POST'])
def addrec():
     if request.method == 'POST':
       try:
          Email_address = request.form['email']
          Username = request.form['uname']
          Password= request.form['password']
          PhoneNo= request.form['pno']

          with sql.connect("main.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO register(Email_address,Username,Password,PhoneNo)VALUES(?,?,?,?)",(Email_address,Username,Password,PhoneNo))
            con.commit()
            msg = "Congrats! You have successfully registered, please login :)"
            return render_template("page-login.html", msg=msg)
            con.close()
       except:
           #return redirect(url_for('signup'))
           message = "Account already exists, please use different Username"
           return render_template("register.html",message = message)
           

#..........................login page......................
@app.route('/search', methods = ['POST'])
def search():
    con = sql.connect("main.db")
    MyUser= request.form['username']
    Password= request.form['password']
    #con.row_factory = sql.Row
    cur = con.cursor()
    query = ("select Password from register where Username = '{MyUser}'").format(MyUser=MyUser)
    cur.execute(query)
    a = cur.fetchone();
    ta=str(a)
    output=ta[2:-3]
    

    if (MyUser=="Hemanth") & (Password=="hemanth@123"):
      session['user']=MyUser
      return render_template("admin.html",username=MyUser)


    if Password==output:
       #result = "Login Successful"
       session['user']=MyUser
       return render_template("Dashboard.html",username=session['user'])
    else:
       error = "Invalid Username or Password :("
       return render_template("page-login.html",error = error)

#................................delete record.....................................
@app.route('/delete', methods = ['POST'])
def delete():
  con = sql.connect("main.db")
  MyUser = request.form['username']
  cur = con.cursor()
  query = ("delete from register where Username = '{MyUser}'"). format(MyUser=MyUser)
  cur.execute(query)
  rows = cur.fetchall();
  return render_template("tables-data.html", rows=rows)

#.............feedback page..................
@app.route('/feed', methods = ['POST'])
def feed():
    con = sql.connect("main.db")
    Full_Name = request.form['fullname']
    Email_address = request.form['email']
    Message = request.form['message']
    cur = con.cursor()
    cur.execute("INSERT INTO feedback(Full_Name,Email_address,Message)VALUES(?,?,?)",(Full_Name,Email_address,Message))
    con.commit()
    con.close()
    return render_template("main.html")

#...................forgot password............
@app.route('/forg', methods = ['POST'])
def forg():
    con = sql.connect("main.db")
    Email_address = request.form['emailid']
    PhoneNo = request.form['phone']
    cur = con.cursor()
    cur.execute("INSERT INTO forget_password(Email_address,PhoneNo)VALUES(?,?)",(Email_address,PhoneNo))
    con.commit()
    con.close()
    return render_template("main.html")

#.............................MCQ part...................
numberOfQuestions = 10
tmp = open('questions.json')
qns = json.load(tmp)

@app.route('/getQuestions/',methods=['POST'])
def getQuestions():
    sectionId = request.form['sectionId']

    sections = ["section1","section2","section3"]


    questions =  random.sample(qns[sectionId],numberOfQuestions)

    #Find the next section
    if sections.index(sectionId)==len(sections)-1:
        Next = "Finish"
    else:
        Next = sections[sections.index(sectionId)+1]

    return jsonify(qns=questions,next=Next)


@app.route('/index')
def index():
    #return make_response(send())
    #headers = {'Content-Type': 'text/html'}
  return render_template('index2.html')
#..........................................tables(database).............................................................................

@app.route('/list')
def list():
  con = sql.connect("main.db")
  con.row_factory = sql.Row

  cur = con.cursor()
  cur.execute("select * from register")

  rows = cur.fetchall();
  return render_template("tables-data.html",rows = rows)
#.........................inserting test1 result into database.........................
@app.route('/sub_res1', methods = ['GET'])
def sub_res1():
    con = sql.connect("main.db")
    correct = int(request.args.get('correct'))
    testname = request.args.get('testname')
    currentTime = datetime.datetime.now()
    resultstatus = "Failed"
    if correct > 6:
      resultstatus = "Passed"
    print('*****************',testname,correct,resultstatus)
    cur = con.cursor()
    cur.execute("INSERT INTO result(username,correct,testname,timestamps,Status)VALUES(?,?,?,?,?)",(g.user,correct,testname,currentTime,resultstatus,))
    con.commit()
    con.close()
    return redirect("/dashboard")
#...............................inserting test2 results into database...................
@app.route('/sub_res', methods = ['GET'])
def sub_res():
    con = sql.connect("main.db")
    correct = int(request.args.get('correct'))
    testname = request.args.get('testname')
    currentTime = datetime.datetime.now()
    resultstatus = "Failed"
    if correct > 6:
      resultstatus = "Passed"
    print('*****************',testname,correct,resultstatus)
    cur = con.cursor()
    cur.execute("INSERT INTO result(username,correct,testname,timestamps,Status)VALUES(?,?,?,?,?)",(g.user,correct,testname,currentTime,resultstatus,))
    con.commit()
    con.close()
    return redirect("/dashboard")
    

#...............................inserting test3 results into database...................
@app.route('/sub_res2', methods = ['GET'])
def sub_res2():
    con = sql.connect("main.db")
    correct = int(request.args.get('correct'))
    testname = request.args.get('testname')
    currentTime = datetime.datetime.now()
    resultstatus = "Failed"
    if correct > 6:
      resultstatus = "Passed"
    print('*****************',testname,correct,resultstatus)
    cur = con.cursor()
    cur.execute("INSERT INTO result(username,correct,testname,timestamps,Status)VALUES(?,?,?,?,?)",(g.user,correct,testname,currentTime,resultstatus,))
    con.commit()
    con.close()
    return redirect("/dashboard")
   
#...............................inserting test4 results into database...................
@app.route('/sub_res3', methods = ['GET'])
def sub_res3():
    con = sql.connect("main.db")
    correct = int(request.args.get('correct'))
    testname = request.args.get('testname')
    currentTime = datetime.datetime.now()
    resultstatus = "Failed"
    if correct > 6:
      resultstatus = "Passed"
    print('*****************',testname,correct,resultstatus)
    cur = con.cursor()
    cur.execute("INSERT INTO result(username,correct,testname,timestamps,Status)VALUES(?,?,?,?,?)",(g.user,correct,testname,currentTime,resultstatus,))
    con.commit()
    con.close()
    return redirect("/dashboard")
    
if __name__=='__main__':
  app.run(debug=True,host='127.0.0.1',port=5000)
