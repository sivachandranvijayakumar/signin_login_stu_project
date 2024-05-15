from flask import Flask,redirect,render_template,request,url_for,session,flash
from flask_mysqldb import MySQL

app=Flask(__name__)

app.secret_key="siva123@"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Siva1234@'
app.config['MYSQL_DB'] = 'student'

mysql = MySQL(app)


def isloggedin():
    return 'username' in session


@app.route("/")
def navbar():
    return render_template("navbar.html") 


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password  


@app.route("/signup/",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        username=request.form["username"] 
        password=request.form["password"]

        cur=mysql.connection.cursor()
        cur.execute('select id from signup where username = %s', (username,))
        old_user = cur.fetchone()
        if old_user:
            cur.close()
            flash('Username already taken. Please choose a different one.', 'danger')
            return render_template('signup.html')
        cur.execute('insert into signup (username, password) values  (%s, %s)', (username, password))
        mysql.connection.commit()
        cur.close()
        flash('Signup Successful', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')
        

@app.route("/login/",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form["username"] 
        password=request.form["password"]

        cur=mysql.connection.cursor()
        cur.execute("select id,username,password from signup where username=%s",(username,))
        login_data=cur.fetchone()
        cur.close()
        if login_data and login_data[2] == password:
            user=User(id=login_data[0],username=login_data[1],password=login_data[2])
            session["username"]=user.username
            
            flash("Login Successful","Success")
            return redirect(url_for("table_fun"))
        else:
            flash("Invalid Credentials","Danger")
    return render_template("login.html")


@app.route("/table/",methods=["GET","POST"])
def table_fun():
    if isloggedin():
        username = session['username']
        cur = mysql.connection.cursor()
        cur.execute('select * from detail where username=%s',(username,))
        data = cur.fetchall()
        cur.close()
        print(data)
        return render_template('table.html', data=data)


@app.route("/add/",methods=["GET","POST"])
def add():
    if request.method=="POST":
        name=request.form["name"]
        age=request.form["age"]
        roll_no=request.form["roll_no"]
        grade=request.form["grade"]

        cur = mysql.connection.cursor()
        cur.execute('insert into detail (username,age,roll_no,grade) values (%s,%s,%s,%s)',(name,age,roll_no,grade))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("table_fun"))
    return render_template("add.html")


@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from detail where id = %s', (id,))
    data = cur.fetchone()
    cur.close()

    if request.method=="POST":
        name=request.form["name"]
        age=request.form["age"]
        roll_no=request.form["roll_no"]
        grade=request.form["grade"]

        cur = mysql.connection.cursor()
        cur.execute('update detail set username=%s, age=%s, roll_no=%s, grade=%s where id=%s', (name, age, roll_no, grade, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("table_fun"))
    return render_template("edit.html",data=data)



@app.route("/delete/<int:id>",methods=["GET","POST"])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from detail where id = %s', (id,))
    mysql.connection.commit() 
    cur.close()
    return redirect(url_for("table_fun"))


@app.route('/logout/')
def logout():
    session.pop('username', None) 
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

if __name__=="__main__":
    app.run(debug=True)
    