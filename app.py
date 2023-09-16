from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from sqlalchemy import DateTime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle image upload
        uploaded_image = request.files["image"]

        # Send the image to the image recognition API
        # Extract the fruit information from the API response

        # Send the identified fruit to the expiry date API
        # Extract the expiry date information from the API response

        # return render_template("result.html", fruit=identified_fruit, expiry_date=expiry_date)

    # If the request method is not POST or after processing POST, always render the index.html template.
    return render_template("index.html")


@app.route('/list')
def show_inventory():
    # Query the database to retrieve all items
    items = Item.query.all()

    # Pass the items to the "list.html" template
    return render_template('list.html', items=items)

@app.route('/add_food', methods=['POST'])
def add_food():
    if request.method == 'POST':
        food_name = request.form['food_name']

        # Create a new Food object and add it to the database
        new_food = Item(name=food_name)
        db.session.add(new_food)
        db.session.commit()

        return redirect(url_for('list.html'))


if __name__ == "__main__":
    app.run(debug=True)
