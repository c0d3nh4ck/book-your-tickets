from flask import Flask, render_template, request, url_for, redirect, session
import pymysql.cursors
import os

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='db1',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
                             
app = Flask(__name__)

#Initialization of variables to use
s = 0
a = 0
b = 0
c = 0
Id = 0

#Route to homepage   
@app.route('/')
def home():    
    return render_template('home.html', s=s, a=a, b=b, c=c)


#Route for handling user signup page logic    
@app.route('/signup_user',methods=['POST', 'GET'])
def signup_user():
    if request.method=='POST':
        EMAIL=request.form['email']
        PASSWORD=request.form['password']
        try:
            with connection.cursor() as cursor:
            # Read a single record
                sql1 = "INSERT INTO db (EMAIL,PASSWORD) VALUES ( %s, %s)" 
                print(sql1, (EMAIL,PASSWORD))
                cursor.execute(sql1, (EMAIL,PASSWORD))
                connection.commit()
        finally:
            return redirect(url_for('login_user'))
    else:
        return render_template('signup_user.html')

#Route for handling theatre owner signup page logic
@app.route('/signup_theatre', methods=['POST','GET'])
def signup_theatre():
    if request.method=='POST':
        Username=request.form['username']
        Theatre_Name=request.form['name']
        Place=request.form['place']
        Password=request.form['password']  
        try:
            with connection.cursor() as cursor:
            # Read a single record    
                sql2 = "INSERT INTO Theatres (Username, Theatre Name, Place, Password) VALUES ( %s, %s, %s, %s)"
                print(sql2, (Username, Theatre_Name, Place, Password))
                cursor.execute(sql2, (Username, Theatre_Name, Place, Password))
                connection.commit() 
        finally:
            return redirect(url_for('login_theatre'))
    else:
        return render_template('signup_theatre.html')             

#Route for handling the login page for user
@app.route('/login_user', methods=['GET', 'POST'])  
def login_user():
    if request.method=='POST':
        Password = request.form['password']
        Email = request.form['email']
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM db WHERE PASSWORD = %s AND EMAIL = %s', (Password, Email))
            results = cursor.fetchall()
        if (results):
            global Id
            for row in results:
                Id = row['ID']
            session['logged_in_u'] = True
            global s 
            s = True
            global a 
            a = True
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login_user'))    
    else:
        return render_template('login_user.html')

#Route for handling the login page for theatre owner
@app.route('/login_theatre', methods=['GET','POST'])
def login_theatre():
    if request.method=='POST':
        Password = request.form['password']
        Username = request.form['username']
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM Theatres WHERE Password = %s AND Username = %s', (Password, Username))
            results = cursor.fetchall()
        if (results):
            global Id
            for row in results:
                Id = row['ID']
            session['logged_in_t'] = True
            global s 
            s = True
            global b 
            b = True
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login_theatre'))
    else:
        return render_template('login_theatre.html')            

#Route for login of admin
@app.route('/login_admin', methods=['GET','POST'])
def login_admin():
    if request.method=='POST':
        Password = request.form['password']
        Username = request.form['admin_id']
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM admin_cred WHERE Password = %s AND Username = %s', (Password, Username))
            results = cursor.fetchall()
        if (results):
            global Id
            for row in results:
                Id = row['ID']
            session['logged_in_a'] = True
            global s 
            s = True
            global c 
            c = True
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login_admin'))
    else:
        return render_template('login_admin.html')

#Route for logout
@app.route('/logout')
def logout():
    if 'logged_in_u' in session:
        session.pop('logged_in_u',None)
        global s 
        global a
        s = False
        a = s
        return redirect(url_for('home'))
    elif 'logged_in_t' in session:
        session.pop('logged_in_t',None)
        global b
        s = False
        b = s
        return redirect(url_for('home')) 
    elif 'logged_in_a' in session:
        session.pop('logged_in_a',None)
        global c
        s = False
        c = s
        return redirect(url_for('home'))        
    else:
        return 'already logged out'    

#Route for user page
@app.route('/user', methods=['GET','POST']) 
def userpage():
    if 'logged_in_u' in session:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM db WHERE ID = %s', (Id))
            details1 = cursor.fetchall()
            cursor.execute('SELECT * FROM Movies')
            details2 = cursor.fetchall()
        for row in details1:
            u = row['EMAIL']         
        return render_template('user.html', u = u, movie = details2) 
    else:
        return redirect(url_for('login_user'))    

#Route for theatre owner page
@app.route('/theatre', methods=['GET','POST'])
def theatre():
    if request.method == 'GET':
        if 'logged_in_t' in session:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM Theatres WHERE ID = %s', (Id))
                details1 = cursor.fetchall()
            for row in details1:
                u = row['Username']
                t = row['Theatre Name']
                p = row['Place']
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM Movie_Req WHERE Theatre_Name = %s', (t))    
                details2 = cursor.fetchall()    
            return render_template('theatre_owner.html', u=u, t=t, m=details2)  
        else:
            return redirect(url_for('login_theatre')) 
    else:
        image = request.form['Upload']
        showtime = request.form['Showtime']
        movie_name = request.form['Movie_Name']
        movie_type = request.form['Movie_Type']  
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM Theatres WHERE ID = %s', (Id))
                details = cursor.fetchall()
            for row in details:
                t = row['Theatre Name']
            with connection.cursor() as cursor:
            # Read a single record    
                sql3 = "INSERT INTO Movies (Theatre_Name, Movie_Name, Movie_Type, Image_dir, Showtime) VALUES (%s, %s, %s, %s, %s)"
                print(sql3, (t, movie_name, movie_type, image, showtime))
                cursor.execute(sql3, (t, movie_name, movie_type, image, showtime))
                connection.commit() 
        finally:
            return redirect(url_for('home'))

#sending movie request
@app.route('/theatre/movie_req', methods=['GET','POST'])
def movie_req():
    if request.method == 'GET':
        if 'logged_in_t' in session:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM Theatres WHERE ID = %s', (Id)) 
                details1 = cursor.fetchall()
            for row in details1:
                t = row['Theatre Name']
                u = row['Username']
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM Movie_Req WHERE Theatre_Name = %s', (t))    
                details2 = cursor.fetchall()
            return render_template('movie_req.html', m=details2, u=u)  
        else:
            return redirect(url_for('login_theatre'))
    else:
        movie = request.form['Movie']
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM Theatres WHERE ID = %s', (Id)) 
            details1 = cursor.fetchall()
        for row in details1:
            t = row['Theatre Name']        
        try:
            with connection.cursor() as cursor:
                sql4 = "INSERT INTO Movie_Req (Movie_Name, Theatre_Name) VALUES (%s, %s)"
                print(sql4, (movie, t))
                cursor.execute(sql4, (movie, t))
                connection.commit()
        finally:
            return redirect(url_for('home'))


#Route to admin page
@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'GET':
        if 'logged_in_a' in session:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM Movie_Req')
                req = cursor.fetchall()
            return render_template('admin.html', req = req)  
        else:
            return redirect(url_for('login_admin'))

@app.route('/admin/<Id>', methods=['GET'])
def req(Id):
    with connection.cursor() as cursor:
        sql5 = 'UPDATE Movie_Req SET Request=%s WHERE ID = %s'
        cursor.execute(sql5,(1, (Id)))
        connection.commit()    
    return redirect(url_for('admin'))

@app.route('/admin/<Id>/remove', methods=['GET'])
def rem(Id):
    with connection.cursor() as cursor:
        sql5 = 'DELETE FROM Movie_Req WHERE ID = %s'
        cursor.execute(sql5,(Id))
        connection.commit()    
    return redirect(url_for('admin'))      



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)                             