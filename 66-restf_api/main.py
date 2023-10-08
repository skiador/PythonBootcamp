import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)
super_secret_api_key = "Hello"


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")
    

# HTTP GET - Read Record
@app.route('/random')
def get_random():
    data = db.session.query(Cafe).all()
    random_cafe = data[random.randint(1, len(data))]
    return jsonify(rand_cafe=random_cafe.to_dict())


@app.route('/all')
def get_all():
    data = db.session.query(Cafe).all()
    all_cafes = [cafe.to_dict() for cafe in data]
    return jsonify(all_cafes)

@app.route("/search")
def search():
    query = request.args.get('loc')
    cafes = db.session.query(Cafe).where(Cafe.location == query).all()
    result = [cafe.to_dict() for cafe in cafes]
    if len(result) == 0:
        return jsonify(
            error="We do not have coffees in this location"
        )
    return jsonify(result)


# HTTP POST - Create Record

@app.route("/add", methods=["POST"])
def add_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        has_sockets=bool(request.form.get("has_sockets")),
        has_toilet=bool(request.form.get("has_toilet")),
        has_wifi=bool(request.form.get("has_wifi")),
        can_take_calls=bool(request.form.get("can_take_calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


# HTTP PUT/PATCH - Update Record
@app.route('/update-price/<cafe_id>', methods=["PATCH"])
def modify_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.get_or_404(Cafe, cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"succes": "Price updated correctly"})
    else:
        return jsonify(error={"Not found": "The cofe id provided does not exist"})


# HTTP DELETE - Delete Record

@app.route('/report-closed/<cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id):
    api_key_provided = request.args.get("api_key")
    if api_key_provided != super_secret_api_key:
        return jsonify(error={"Invalid key": "The api key provided is not valid"})
    else:
        cafe = db.get_or_404(Cafe, cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"Succes": "Cafe deleted correctly"})
        return jsonify(error={"Error": "No cafe with the specified id in the database"})
    pass


if __name__ == '__main__':
    app.run(debug=True)
