from flask import Flask, render_template, url_for
from post import Post
import requests

app = Flask(__name__)

URL = "https://api.npoint.io/c790b4d5cab58020d391"
connection = requests.get(URL)
blogs_json = connection.json()
posts_list = []
for blog in blogs_json:
    post = Post(blog)
    posts_list.append(post)

@app.route('/')
def home():
    return render_template("index.html", blogs=posts_list)

@app.route('/post/<post_id>')
def get_post(post_id):
    return render_template("post.html", post=posts_list[int(post_id)])

if __name__ == "__main__":
    app.run(debug=True)
