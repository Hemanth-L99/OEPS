from flask import Flask, render_template, flash,request, redirect, url_for, make_response, jsonify, json,jsonify, session
from flask import make_response, request, current_app, redirect, url_for, send_from_directory, g
import os,time,datetime
import  random
import sqlite3 as sql

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

@app.route('/result')
def check():
  if g.user:
    con = sql.connect('C:/Users/lanka/Desktop/ignou project/Sem 6/Hemanth/main.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from result where username=?",(g.user,))
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

          with sql.connect("C:/Users/lanka/Desktop/ignou project/Sem 6/Hemanth/main.db") as con:

            cur = con.cursor()
            cur.execute("INSERT INTO register(Email_address,Username,Password,PhoneNo)VALUES(?,?,?,?)",(Email_address,Username,Password,PhoneNo))
            con.commit()
            con.close()
            msg = "Congrats! You have successfully registered, please login :)"
            return render_template("page-login.html", msg=msg)
       except:
           #return redirect(url_for('signup'))
           message = "Account already exists, please use different Username"
           return render_template("register.html",message = message)
           

#..........................login page......................
@app.route('/search', methods = ['POST'])
def search():
    con = sql.connect("C:/Users/lanka/Desktop/ignou project/Sem 6/Hemanth/main.db")
    MyUser= request.form['username']
    Password= request.form['password']
    #con.row_factory = sql.Row
    cur = con.cursor()
    query = ("select Password from register where Username = '{MyUser}'").format(MyUser=MyUser)
    cur.execute(query)
    a = cur.fetchone();
    ta=str(a)
    output=ta[2:-3]
    

    if (MyUser=="LHemanth") & (Password=="godsay@123"):
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
  con = sql.connect("C:/Users/lanka/Desktop/ignou project/Sem 6/Hemanth/main.db")
  MyUser = request.form['username']
  cur = con.cursor()
  query = ("delete from register where Username = '{MyUser}'"). format(MyUser=MyUser)
  cur.execute(query)
  rows = cur.fetchall();
  return render_template("tables-data.html", rows=rows)

#.............feedback page..................
@app.route('/feed', methods = ['POST'])
def feed():
    con = sql.connect("C:/Users/lanka/Desktop/ignou project/Sem 6/Hemanth/main.db")
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
    con = sql.connect("C:/Users/lanka/Desktop/ignou project/Sem 6/Hemanth/main.db")
    Email_address = request.form['emailid']
    PhoneNo = request.form['phone']
    cur = con.cursor()
    cur.execute("INSERT INTO forget_password(Email_address,PhoneNo)VALUES(?,?)",(Email_address,PhoneNo))
    con.commit()
    con.close()
    return render_template("main.html")

#.............................MCQ part...................
numberOfQuestions = 10
qns = {
    "section1": [
                ["q1","- Two trains running in opposite directions cross a man standing on the platform in 27 seconds and 17 seconds respectively and they cross each other in 23 seconds. The ratio of their speeds is:?",["200 m","225 m","245 m","250 m"],"245 m"],
                ["q2","- Two, trains, one from Howrah to Patna and the other from Patna to Howrah, start simultaneously. After they meet, the trains reach their destinations after 9 hours and 16 hours respectively. The ratio of their speeds is:?",["2:3","4:3","6:7","9:16"],"4:3"],
                ["q3","- A man standing at a point P is watching the top of a tower, which makes an angle of elevation of 30º with the man's eye. The man walks some distance towards the tower to watch its top and the angle of the elevation becomes 60º. What is the distance between the base of the tower and the point P?",["4(3)^1/2 units","8 units","12 units","Data inadequate"],"d"],
                ["q4","- A, B and C jointly thought of engaging themselves in a business venture. It was agreed that A would invest Rs. 6500 for 6 months, B, Rs. 8400 for 5 months and C, Rs. 10,000 for 3 months. A wants to be the working member for which, he was to receive 5% of the profits. The profit earned was Rs. 7400. Calculate the share of B in the profit.",["Rs. 1900","Rs. 2660","Rs. 2800","Rs. 2840"],"b"],
                ["q5","- A vendor bought toffees at 6 for a rupee. How many for a rupee must he sell to gain 20%?",["3","4","5","6"],"c"],
                ["q6","- In a certain store, the profit is 320%  of the cost. If the cost increases by 25% but the selling price remains constant, approximately what percentage of the selling price is the profit?",["30%","70%","100%","250%"],"b"],
                ["q7","- When a plot is sold for Rs. 18,700, the owner loses 15%. At what price must that plot be sold in order to gain 15%?",["Rs. 21,000","Rs. 22,500","Rs. 25,300","Rs. 25,800"],"c"],
                ["q8","- What was the day of the week on 17th June, 1998?",["Monday","Tuesday","Wednesday","Thursday"],"c"],
                ["q9","- Today is Monday. After 61 days, it will be:?",["Wednesday","Saturday","Tuesday","Thursday"],"b"],
                ["q10","- On what dates of April, 2001 did Wednesday fall?",["1st, 8th, 15th, 22nd, 29th","2nd, 9th, 16th, 23rd, 30th","3rd, 10th, 17th, 24th","4th, 11th, 18th, 25th"],"d"],
                ["q11","- Three pipes A, B and C can fill a tank from empty to full in 30 minutes, 20 minutes, and 10 minutes respectively. When the tank is empty, all the three pipes are opened. A, B and C discharge chemical solutions P,Q and R respectively. What is the proportion of the solution R in the liquid in the tank after 3 minutes?",["5/11","6/11","7/11","8/11"],"b"],
                ["q12","- A large tanker can be filled by two pipes A and B in 60 minutes and 40 minutes respectively. How many minutes will it take to fill the tanker from empty state if B is used for half the time and A and B fill it together for the other half?",["15 min","20 min","27.5 min","30 min"],"d"],
                ["q13","- Let N be the greatest number that will divide 1305, 4665 and 6905, leaving the same remainder in each case. Then sum of the digits in N is:?",["4","5","6","8"],"a"],
                ["q14","- The greatest number of four digits which is divisible by 15, 25, 40 and 75 is:?",["9000","9400","9600","9800"],"c"],
                ["q15","- The least number, which when divided by 12, 15, 20 and 54 leaves in each case a remainder of 8 is:?",["504","536","544","548"],"d"]
                ],
    "section2": [
                ["q21","what is root of 22552?",["a","b","c","d"],"d"],
                ["q22","Look at this series: 2, 1, (1/2), (1/4), ... What number should come next?",["1/3","1/8","2/8","1/16"],"b"],
                ["q23","B2CD, _____, BCD4, B5CD, BC6D",["B2C2D","BC3D","B2C3D","BCD7"],"b"],
                ["q24","3 pumps, working 8 hours a day, can empty a tank in 2 days. How many hours a day must 4 pumps work to empty the tank in 1 day?",["9","10","11","12"],"d"],
                ["q25","Running at the same constant rate, 6 identical machines can produce a total of 270 bottles per minute. At this rate, how many bottles could 10 such machines produce in 4 minutes?",["648","1800","270","8898"],"b"],
                ["q26","9 persons can repair a road in 12 days, working 5 hours a day. In how many days will 30 persons, working 6 hours a day, complete the work?",["10","14","13","16"],"c"],
                ["q27","If a quarter kg of potato costs 60 paise, how many paise will 200 gm cost?",["48 paise","54 paise","56 paise","72 paise"],"a"],
                ["q28","A wheel that has 6 cogs is meshed with a larger wheel of 14 cogs. When the smaller wheel has made 21 revolutions, then the number of revolutions mad by the larger wheel is:",["4","12","9","29"],"c"],
                ["q29","If 7 spiders make 7 webs in 7 days, then 1 spider will make 1 web in how many days?",["1","7/2","7","49"],"c"],
                ["q30","In a camp, there is a meal for 120 men or 200 children. If 150 children have taken the meal, how many men will be catered to with remaining meal?",["20","30","40","50"],"b"],
                ["q31","An industrial loom weaves 0.128 metres of cloth every second. Approximately, how many seconds will it take for the loom to weave 25 metres of cloth?",["178","195","204","488"],"b"],
                ["q32","36 men can complete a piece of work in 18 days. In how many days will 27 men complete the same work?",["12","18","22","24"],"d"]
                ],
    "section3": [
                ["q41","What is your name?",["Ram","Prem","Raghu","peter"],"Prem"],
                ["q42","Where are you?",["bangalore","Pune","Chennai"],"bangalore"],
                ["q43","What is your fav food?",["a","b","c","d"],"b"],
                ["q44","q4?",["a","b","c","d"],"b"],
                ["q45","q5?",["a","b","c","d"],"b"],
                ["q26","26?",["a","b","c","d"],"b"],
                ["q27","27?",["a","b","c","d"],"b"],
                ["q28","28?",["a","b","c","d"],"b"],
                ["q29","29?",["a","b","c","d"],"b"],
                ["q30","30?",["a","b","c","d"],"b"]
                ],
    "section4": [
                ["q61","What is your name?",["Ram","Prem","Raghu","peter"],"Prem"],
                ["q62","Where are you?",["bangalore","Pune","Chennai"],"bangalore"],
                ["q63","What is your fav food?",["a","b","c","d"],"b"],
                ["q64","q4?",["a","b","c","d"],"b"],
                ["q65","q5?",["a","b","c","d"],"b"]
                ],
    "section5": [
                ["q81","What is your name?",["Ram","Prem","Raghu","peter"],"Prem"],
                ["q82","Where are you?",["bangalore","Pune","Chennai"],"bangalore"],
                ["q83","What is your fav food?",["a","b","c","d"],"b"],
                ["q84","q4?",["a","b","c","d"],"b"],
                ["q85","q5?",["a","b","c","d"],"b"]
                ]

}
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
  con = sql.connect("C:/Users/lanka/Desktop/ignou project/Sem 6/Hemanth/main.db")
  con.row_factory = sql.Row

  cur = con.cursor()
  cur.execute("select * from register")

  rows = cur.fetchall();
  return render_template("tables-data.html",rows = rows)

#...............................inserting test2 results into database...................
@app.route('/sub_res', methods = ['GET'])
def sub_res():
    con = sql.connect("C:/Users/lanka/Desktop/ignou project/Sem 6/Hemanth/main.db")
    correct = request.args.get('correct')
    testname = request.args.get('testname')
    print('*****************',testname,correct)
    cur = con.cursor()
    cur.execute("INSERT INTO result(username,correct,testname)VALUES(?,?,?)",(g.user,correct,testname,))
    con.commit()
    con.close()
    return redirect("/dashboard")
    

#...............................inserting test3 results into database...................
@app.route('/sub_res2', methods = ['GET'])
def sub_res2():
    con = sql.connect("C:/Users/lanka/Desktop/ignou project/Sem 6/Hemanth/main.db")
    correct = request.args.get('correct')
    testname = request.args.get('testname')
    print('*',testname,correct)
    cur = con.cursor()
    cur.execute("INSERT INTO result(username,correct,testname)VALUES(?,?,?)",(g.user,correct,testname,))
    con.commit()
    con.close()
    return redirect("/dashboard")
   
#...............................inserting test4 results into database...................
@app.route('/sub_res3', methods = ['GET'])
def sub_res3():
    con = sql.connect("C:/Users/lanka/Desktop/ignou project/Sem 6/Hemanth/main.db")
    correct = request.args.get('correct')
    testname = request.args.get('testname')
    print('*',testname,correct)
    cur = con.cursor()
    cur.execute("INSERT INTO result(username,correct,testname)VALUES(?,?,?)",(g.user,correct,testname,))
    con.commit()
    con.close()
    return redirect("/dashboard")
    
if __name__=='__main__':
  app.run(debug=True,host='127.0.0.1',port=5000)
