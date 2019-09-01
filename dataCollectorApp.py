import psycopg2
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app=Flask(__name__)

##app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:3962731@localhost/Height_collector'
##app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']='postgres://nvcdrwfhqoxucx:407eb4517636f7eec2e28f79c4610b26c323180b38153bd405acf790bd7c0d79@ec2-174-129-242-183.compute-1.amazonaws.com:5432/dfpqgu3lodavd8?sslmode=require'

db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(120), unique=True)
    height_ = db.Column(db.Integer)


    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        email=request.form["email_name"]
        height=request.form["height_name"]
        if db.session.query(Data).filter(Data.email_==email).count() == 0:
            data = Data(email,height)
            db.session.add(data)
            db.session.commit()
            average_height =  db.session.query(func.avg(Data.height_)).scalar()
            average_height = round(average_height, 2)
            count=db.session.query(Data.height_).count()
            send_email(email, height, average_height, count)
            return render_template("success.html")
        else:
            return render_template("index.html",
            text = "Seems like you have entered this email before, try a new one!")

if __name__ == '__main__':
     app.debug=True
     app.run()

