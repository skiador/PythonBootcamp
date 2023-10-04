from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv
import pandas as pd

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField('Location Url', validators=[URL()])
    open_time = StringField('Open Time', validators=[DataRequired()])
    closing_time = StringField('Closing Time', validators=[DataRequired()])
    coffee_rating = SelectField(
        "Coffee Rating",
        choices=[("☕"*i, "☕"*i) for i in range(5) if i != 0],
        validators=[DataRequired()]
    )
    wifi_rating = SelectField(
        "Wifi Rating",
        choices=[("✘", "✘")] + [("💪"*i, "💪"*i) for i in range(5) if i != 0],
        validators=[DataRequired()]
    )
    power = SelectField(
        "Power",
        choices=[("✘", "✘")] + [("🔌"*i, "🔌"*i) for i in range(5) if i != 0],
        validators=[DataRequired()])
    submit = SubmitField('Submit')



# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", "a", newline='') as data:
            csv_writer = csv.writer(data)
            data_to_append = [field.data for field in form if field != "submit"]
            csv_writer.writerow(data_to_append)
            data.close()
        return redirect(url_for('cafes'))
    else:
        return render_template('add.html', form=form)



@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
