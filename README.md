# HTNXTAFH
Theodore, Helen, Alex, Freddy

## How to run
1. Install the requirements
2. Init the database with `flask db init`
3. Then prep the database with `flask db migrate` and `flask db upgrade`
4. Run the flask server with `python app.py`

## How to connect phone to computer to demo it from the phone
1. Set the phone as a hotspot
2. Connect the computer to the phone's hotspot
3. Make sure that in app.py, the host is set to 0.0.0.0
4. Take the secondary ip in the print when the server starts
5. On the phone, go to the ip address of the computer and the port 8000 like the print says
6. Proffit.