from flask import Flask, render_template, request
from posts import Post
import requests
import smtplib
import os


MY_EMAIL = os.environ["MY_EMAIL"]
PASSWORD = os.environ["PASSWORD"]
SMTP = "smtp.gmail.com"


app = Flask(__name__)

# Import all blog entries and create Post objects
URL = "https://api.npoint.io/16e7dbc3f8f4a1484900"
connection = requests.get(URL)
json_data = connection.json()
posts_list = []
for entry in json_data:
    post = Post(entry)
    posts_list.append(post)


@app.route("/")
def home():
    return render_template("index.html", posts_list=posts_list)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/post/<int:post_entry>")
def get_post(post_entry):
    return render_template("post.html", post_entry=posts_list[post_entry-1])


@app.route('/form-entry', methods=['POST'])
def receive_data():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    message = request.form["message"]
    email_connection = smtplib.SMTP(SMTP)
    email_connection.starttls()
    email_connection.login(user=MY_EMAIL, password=PASSWORD)
    email_message = f"Subject: New Message\n\n{name}\n{email}\n{phone}\n{message}"
    try:
        email_connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg=email_message)
    except UnicodeError:
        return "<h1>Special characters not allowed. Try again</h1>"
    return "<h1>Message sent successfully!</h1>"
           
        

if __name__ == "__main__":
    app.run(debug=True)