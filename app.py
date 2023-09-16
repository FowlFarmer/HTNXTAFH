from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    if request.method == "POST":
            # Handle image upload
            uploaded_image = request.files["image"]

            # Send the image to the image recognition API
            # Extract the fruit information from the API response

            # Send the identified fruit to the expiry date API
            # Extract the expiry date information from the API response

            # return render_template("result.html", fruit=identified_fruit, expiry_date=expiry_date)

            return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
