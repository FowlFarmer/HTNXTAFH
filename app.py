from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from sqlalchemy import DateTime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import expiry_finder_cohere
import food_recognition_mp
import receipt_recognizer
import recipie_creator

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

    # Create a new Item object and add it to the database
    new_food = Item(name=food_name, days_for_expiry=expiry_days)
    db.session.add(new_food)
    db.session.commit()

def get_days_until_expiry(item_id):
    item = Item.query.get(item_id)
    if item and item.days_for_expiry != -1:
        days_until_expiry = item.days_for_expiry - (datetime.utcnow() - item.time_of_entry).days
        return days_until_expiry
    else:
        return None
    
def interpret_expiry_date(expiry_date):
    if expiry_date == None:
        return "Unknown"
    elif expiry_date >= 100000:
        return "Never"
    else:
        if expiry_date < 0:
            return f"{abs(expiry_date)} days ago"
        else:
            return f"{expiry_date} days"
    
def expiry_text(item_id):
    return interpret_expiry_date(get_days_until_expiry(item_id))

def ranking_expiry(v):
    if v == None:
        return 9999999999999999999999999999
    else:
        return v

@app.route('/upload', methods=["GET","POST"])
def upload():
    if request.method == 'POST':
        # Get the uploaded image file
        uploaded_image = request.files['image']

        # Check if a file was uploaded
        if uploaded_image.filename != '':
            # Save the uploaded image to a temporary location (optional)
            # Then, call your food classifier function with the image path
            image_path = 'static/temp_image.jpg'  # Temporary file path
            uploaded_image.save(image_path)

            # Call the food classifier function
            food_result = food_recognition_mp.recognise_food(image_path)

            # pass us over to the confirmation page
            return render_template('add_food_confirm.html',foodname=food_result)
    else:
        # Return to the upload page if no file is uploaded or other errors occur
        return render_template("upload.html")  
    

@app.route('/upload-receipt', methods=["POST"])
def upload_receipt():
    if request.method == 'POST':
        # Get the uploaded image file
        uploaded_image = request.files['image']

        # Check if a file was uploaded
        if uploaded_image.filename != '':
            # Save the uploaded image to a temporary location (optional)
            image_path = 'static/temp_receipt.jpg'  # Temporary file path
            uploaded_image.save(image_path)

            # Call the reciept interpreter
            reciept_text = receipt_recognizer.image_to_text(image_path)
            reciept_text = receipt_recognizer.interpret_receipt(reciept_text)

            # pass us over to the confirmation page
            return render_template('add_reciept_confirm.html',reciept_text=reciept_text)
    
@app.route('/add_food_bulk', methods=['POST'])
def add_food_bulk():
    if request.method == 'POST':
        reciept_list = request.form.get('reciept_list')
        reciept_list = reciept_list.replace("\r", "").replace("\n", "")
        split_lit = reciept_list.split(", ")

        for food_name in split_lit:
            add_food_item_db(food_name)
        return redirect(url_for('show_inventory'))


# a simple get request for the temp_image.jpg file
@app.route('/temp_image.jpg', methods=["GET"])
def get_temp_image():
    return app.send_static_file('temp_image.jpg')

# a simple get request for the temp_receipt.jpg file
@app.route('/temp_receipt.jpg', methods=["GET"])
def get_temp_receipt():
    return app.send_static_file('temp_receipt.jpg')

@app.route('/', methods=["GET", "POST"])
def show_inventory():
    if request.method == 'POST':
        # Get the food name from the form
        food_name = request.form['food_name']

        # Add the food to the database
        add_food_item_db(food_name)

        # Redirect to the inventory page
        return redirect(url_for('show_inventory'))
    # Query the database to retrieve all items
    items = Item.query.all()

    # order the items by their expiry time and give unknown at the bottom
    
    items.sort(key=lambda x: ranking_expiry(get_days_until_expiry(x.id)))

    # Pass the items to the "list.html" template
    return render_template('list.html', items=items, expiry_text=expiry_text)


# make an app route for adding food where the name of the item is a param like /add_food?name=apple
@app.route('/add_food', methods=['POST'])
def add_food_post():
    if request.method == 'POST':
        food_name = request.form.get('food_name')
        add_food_item_db(food_name)
        return redirect(url_for('show_inventory'))
    
@app.route('/confirm_food/<string:food_name>', methods=['GET'])
def confrim_food(food_name):
    return render_template('add_food_confirm.html',foodname=food_name)
    

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
    
    
# a route that re-calculates the expiry date of an item if its a weird value
@app.route('/recalculate_expiry/<int:item_id>', methods=['GET', 'POST'])
def recalculate_expiry(item_id):
    # Query the database to find the item by its ID
    item_to_recalculate = Item.query.get(item_id)

    if item_to_recalculate:
        # Delete the item from the database
        item_to_recalculate.days_for_expiry = expiry_finder_cohere.ask_expiry(item_to_recalculate.name)
        db.session.commit()

        return redirect(url_for('show_inventory'))
    else:
        return "Item not found", 404
    
# a page to show the recipie
@app.route('/recipie', methods=['GET'])
def recipie_example(): # if its a GET request, tell them to go back the main screen and select items, same for if they didnt select any items. If its a POST, generate the recipie and show it
    return render_template('recipe.html', recipie="Please go back to the main screen and select some items to make a recipie with.")

@app.route('/auto_recipie', methods=['POST'])
def auto_recipie_post(): 
    recipie = "Please go back to the main screen and select some items to make a recipie with."
    if request.method == 'POST':
        # Get the food name from the form
        integredient_list = request.form['selectedFoodsInput']
        print(integredient_list)
        if len(integredient_list) == 0 or integredient_list == "[]":
            return render_template('recipe.html', recipie=recipie)
        recipie = recipie_creator.generate_recipe(integredient_list)
    return render_template('recipe.html', recipie=recipie)

if __name__ == "__main__":
    app.run(debug=True,port=8000)
