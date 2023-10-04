from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)

# CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-collection.db"

# Create the extension
db = SQLAlchemy()
# Initialise the app with the extension
db.init_app(app)


# CREATE TABLE
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'


# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title))
        all_books = result.scalars()
        rows = db.session.query(Book).count()
        return render_template('index.html', library=all_books, rows=rows)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form.get("name")
        author = request.form.get("author")
        rating = request.form.get("rating")
        new_book = Book(title=name, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit(book_id):
    # Query the book within the current session
    book_to_update = db.session.query(Book).filter_by(id=book_id).first()

    if book_to_update is None:
        return "Book not found"

    if request.method == "POST":
        new_rating = request.form.get("rating")
        try:
            # Convert the user's input to a float
            new_rating = float(new_rating)
        except ValueError:
            # Handle the case where the input is not a valid float
            return "Invalid rating input. Please enter a valid number."

        # Update the book's rating and commit within the same session
        book_to_update.rating = new_rating
        db.session.commit()

        print(f"Updated rating for {book_to_update.title} to {new_rating}")

        return redirect(url_for('home'))

    return render_template("edit.html", book_to_update=book_to_update)


@app.route("/delete/<int:entry_id>", methods=["GET", "POST"])
def delete(entry_id):
    book_to_delete = db.session.query(Book).filter_by(id=entry_id).first()
    if book_to_delete is None:
        return "Book not found"
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

