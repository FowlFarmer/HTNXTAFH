from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from sqlalchemy import DateTime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import expiry_finder_cohere
import food_recognition_mp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    time_of_entry = db.Column(db.DateTime, default=datetime.utcnow)
    days_for_expiry = db.Column(db.Integer)


def add_food_item_db(food_name):
    expiry_days = expiry_finder_cohere.ask_expiry(food_name)

    # Create a new Food object and add it to the database
    new_food = Item(name=food_name, days_for_expiry=expiry_days)
    db.session.add(new_food)
    db.session.commit()

def get_days_until_expiry(item_id):
    item = Item.query.get(item_id)
    if item:
        days_until_expiry = item.days_for_expiry - (datetime.utcnow() - item.time_of_entry).days
        return days_until_expiry
    else:
        return -1

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
    return render_template('list.html', items=items, get_days_until_expiry=get_days_until_expiry)


@app.route('/add_food', methods=['POST'])
def add_food_path():
    if request.method == 'POST':
        food_name = request.form['food_name']
        add_food_item_db(food_name)
        return redirect(url_for('show_inventory'))
    

@app.route('/delete/<int:item_id>', methods=['GET', 'POST']) # WATCH OUT, THIS IS TOTALLY NOT XSS SAFE LIKE WE CAN DELETE ITEMS BUT WHATEVER
def delete_item(item_id):
    # Query the database to find the item by its ID
    item_to_delete = Item.query.get(item_id)

    if item_to_delete:
        # Delete the item from the database
        db.session.delete(item_to_delete)
        db.session.commit()

        return redirect(url_for('show_inventory'))
    else:
        return "Item not found", 404


@app.route('/upload', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        # Get the uploaded image file
        uploaded_image = request.files['image']

        # Check if a file was uploaded
        if uploaded_image.filename != '':
            # Save the uploaded image to a temporary location (optional)
            # Then, call your food classifier function with the image path
            image_path = 'temp_image.jpg'  # Temporary file path
            uploaded_image.save(image_path)

            # Call the food classifier function
            food_result = food_recognition_mp.recognise_food(image_path)
            add_food_item_db(food_result)

            # Return the result to a new template (e.g., result.html)
            return redirect(url_for('show_inventory'))
    # Return to the upload page if no file is uploaded or other errors occur
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
