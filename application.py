
# Main Flask framework 
from flask import Flask
# Contains resources, and apis
from flask_restful import Api

# Note convention of having the list co-exist in the single instance file
from resources.item import Item, ItemList
from resources.queue import Queue

# Creation of main Flask app
app = Flask(__name__)
# Specify the path to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = 'crud_sample'

# Connection of the Flask application to the flask_restful API 
api = Api(app)

# Decorated function that instructs us to create all the tables if they don't exist
@app.before_first_request
def create_tables():
    db.create_all()

# Creation of the REST endpoints (resources) by binding them to the Resource classes
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Queue, '/queue/<string:path_parameter_in_uri>')

# This is invoked because app.py is launched from the command line
if __name__ == '__main__':
	# Import the SQLAlchemy database 
    from db import db
    # Initialize the SQLAlchemy database
    db.init_app(app)
    # Launch the Flask application on port 5000, and turn on verbose debugging
    app.run(port=5000, debug=True)
