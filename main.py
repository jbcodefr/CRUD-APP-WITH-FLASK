from flask import Flask,render_template,request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
#init app
app = Flask(__name__) 

app.config['SECRET_KEY'] = 'xxxxxxxxxxxxxx'
#app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:admin@localhost:3306/flask_dev'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost:5432/flask_dev"
db=SQLAlchemy(app)

#db model
class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(150),unique=True)
    username=db.Column(db.String(150))


def __init__(self,email,username):
    self.email=email
    self.username=username
    
 
 # flask_restful librerie tags
@app.route('/')
def home():
    userlist=User.query.all()
    return render_template("home.html",userlist=userlist)

#insert user function
@app.route('/insert',methods=['GET','POST'])
def insert(): 
    if request.method=='POST':
        email=request.form.get('email')
        username=request.form.get('username')

        check_username=User.query.filter_by(username=username).first()
        check_email=User.query.filter_by(email=email).first()
        if check_username:
            flash('username already Used ',category='error') 
        if check_email:
            flash('Email already Used ',category='error') 
        if len(email)<3:
            flash('_> Email > 4 charac',category='error')
        if len(username)<2:
            flash('_> Username > 4 charac',category='error')
        else:
            new_user=User(email=email,username=username,id=None)
            db.session.add(new_user)
            db.session.commit()
            flash('User: "'+username+'" Created',category='success')
            ##login_user(user,remember=True)
            ## userResult=db.session.query(User)
            return redirect(url_for("home"))
    return render_template("insert.html") 

#update user function
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    uto = User.query.get_or_404(id)
    if request.method=='POST':
        email=request.form.get('email')
        username=request.form.get('username')
        
        if uto.email==request.form.get('email'):
            flash('Email already Used ',category='error') 
        elif len(email)<3:
            flash('_> Email > 4 charac',category='error')
        elif len(username)<2:
            flash('_> Username > 4 charac',category='error')
        else:
            uto.email=request.form.get('email')
            uto.username=request.form.get('username')
            db.session.commit()
            flash('User: "'+uto.username+'" Updated',category='success')
            ##login_user(user,remember=True)
            ## userResult=db.session.query(User)
            return redirect(url_for("home"))
    return render_template("update.html",user=uto) 

#delete user function
@app.route('/delete/<int:id>',methods=['GET','POST'])
def delete_user(id):
        utd = User.query.get_or_404(id)
        username = utd.username
        if utd:
            db.session.delete(utd)
            db.session.commit()
            flash('User: "'+username+'" deleted',category='warning')
            return redirect(url_for("home")) 

if __name__ == '__main__':
    app.run(debug=True)