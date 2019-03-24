from db import db

# The model class responsible for defining the data and the 
# bindings to the ORM (SqlAlchemy)
class ItemModel(db.Model):
    # Specification of the table name 
    __tablename__ = 'items'

    # Creation of the fields (note relationships to vars in constructor)
    # The id will be automatically incremented
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    quantity = db.Column(db.Integer)

    # Example of a relation to another table 
    # item_owner_id = db.Column(db.Integer, db.ForeignKey('item_owner.id'))
    # item_owner = db.relationship('ItemOwnerModel')

    # Constructor
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    # Create the ability for the object to render itself as json
    # and must be a dictionary
    def json(self):
        return {'id': self.id, 'name': self.name, 'quantity': self.quantity}

    # Class-defined convenience method to find the object by its name
    # reminder: cls denotes "class"
    @classmethod
    def find_by_name(cls, name):
        # Example of using the query-builder
        # Equivalent to SELECT * FROM items WHERE name:=name LIMIT 1 
        return cls.query.filter_by(name=name).first()

    # Used to update as well as store the first time
    def save_to_db(self):
        # You can queue up multiple transactions via add() to make more efficient
        db.session.add(self)
        # Does the actual commiting of the transactions to the database 
        db.session.commit()

    # Used to delete the entry from the database
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
