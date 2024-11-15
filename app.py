from datetime import datetime
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import variables

app = Flask(__name__)

app.config["SECRET_KEY"] = "myappkey1234"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = variables.get_username()
app.config["MAIL_PASSWORD"] = variables.get_password()

database = SQLAlchemy(app)

mail = Mail(app)

class Form(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    first_name = database.Column(database.String(50), nullable=False)
    last_name = database.Column(database.String(50), nullable=False)
    email = database.Column(database.String(100), nullable=False)
    available_date = database.Column(database.Date, nullable=False)
    current_status = database.Column(database.String(20), nullable=False)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["firstName"]
        last_name = request.form["lastName"]
        email = request.form["email"]
        available_date = request.form["date"]
        current_status = request.form["currentStatus"]
        date_object = datetime.strptime(available_date, "%Y-%m-%d")

        form = Form(first_name=first_name, last_name=last_name, email=email,
                    available_date=date_object, current_status=current_status)
        database.session.add(form)
        database.session.commit()

        msg = Message("New Form Submission", sender=app.config["MAIL_USERNAME"], recipients=[email], body=f"Thank you for your submission, please find your data below:\n"
                                                                                                          f"First Name: {first_name}\n"
                                                                                                          f"Last Name: {last_name}\n"
                                                                                                          f"Available Date: {available_date}\n"
                                                                                                          f"Current Status:{current_status}\n")
        mail.send(msg)
        flash(f"{first_name}, your form was submitted successfully, we will get back to you soon!", "success")
    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():  # Create a new session
        database.create_all()  # Create the database tables if they don't exist'
        app.run(debug=True, port=5001)
