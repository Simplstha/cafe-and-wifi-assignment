from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv(".env")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    false_url = URL(message="Invalid URL")
    map_url = StringField('Location URL', validators=[DataRequired(), false_url])
    img_url = StringField("Image URL", validators=[DataRequired(), false_url])
    location = StringField('Location', validators=[DataRequired()])
    has_sockets = BooleanField("Has Sockets")
    has_wifi = BooleanField('Has Wifi')
    has_toilet = BooleanField('Has Toilets')
    can_take_calls = BooleanField('Can Take Calls')
    seats = StringField("How many seats does it have?", validators=[DataRequired()])
    coffee_price = StringField("Coffee Price", validators=[DataRequired()])
    submit = SubmitField('Submit')


# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cafes(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(50), nullable=False)
    coffee_price = db.Column(db.String(50), nullable=False)


# with app.app_context():
#     db.create_all()

# all Flask routes below
@app.route("/")
def home():
    cafes = Cafes.query.all()
    return render_template("index.html", cafes=cafes)


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafes(
            name=form.cafe.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_wifi=form.has_wifi.data,
            has_toilet=form.has_toilet.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


@app.route('/cafes/<int:cafe_id>')
def cafes(cafe_id):
    cafe_to_show = Cafes.query.get(cafe_id)
    return render_template('cafes.html', cafe=cafe_to_show)


if __name__ == '__main__':
    app.run(debug=True)
