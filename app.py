from os import name
from flask import Flask,render_template,redirect,url_for,request
import json
from flask_sqlalchemy import SQLAlchemy
import razorpay

app = Flask(__name__)
db=SQLAlchemy(app)
app.config['SECRET_KEY']="topsecret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Users(db.Model):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    email=db.Column(db.String(120), nullable=False)
    name=db.Column(db.String(120), nullable=False)
    amount=db.Column(db.String(120), nullable=False)


@app.route("/", methods=['GET','POST'])
def hello_world():
    if (request.method == "POST"):
        email=request.form.get("email")
        name=request.form.get("uname")
        amount=request.form.get("amount")
        user=Users(email=email,name=name,amount=amount)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('pay',id=user.id))
        # return redirect(url_for('pay',id=amount))

    return render_template('index.html')


@app.route("/suc",methods=['GET','POST'])
def success():
    return render_template('suc.html')


@app.route("/pay/<id>",methods=['GET','POST'])
def pay(id):
    user=Users.query.filter_by(id=id).first()
    client=razorpay.Client(auth=("rzp_test_6EryT0PqkVBbee","g5EP1R2qQkeVrWoFJ3TNe3Fx"))
    payment=client.order.create({'amount':(int(user.amount)*100),'currency':'INR','payment_capture':'1'})
    return render_template('pay.html',payment=payment,name=user.name)
# g5EP1R2qQkeVrWoFJ3TNe3Fx
if __name__=="__main__":
    app.debug=True
    db.create_all()
    app.run()
    FLASK_APP=app.py