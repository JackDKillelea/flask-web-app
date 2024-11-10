from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["firstName"]
        last_name = request.form["lastName"]
        email = request.form["email"]
        available_date = request.form["date"]
        current_status = request.form["currentStatus"]
        print(first_name)
        print(last_name)
        print(email)
        print(available_date)
        print(current_status)

    return render_template("index.html")

app.run(debug=True, port=5001)
