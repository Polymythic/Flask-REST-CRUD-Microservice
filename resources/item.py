# The resource file should only service the API.  The model shou;d
# handle all lifting associated to the underlying resource

# Import for resource creation and for a request parser 
from flask_restful import Resource, reqparse
# Get the model associated with this resource
from models.item import ItemModel

class Item(Resource):
    # Create a class-wide request parser
    parser = reqparse.RequestParser()
    # Specify which fields are being sent in the body of the request and if they are required
    parser.add_argument('quantity',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    # Each method corresponds to an HTTP verb corresponding to the call
    # This is what flask_restful provides
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        # flask_restful calls must return a serializable tuple - 404 is client-side error
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        # Invoke the class's parser 
        data = Item.parser.parse_args()

        # Use argument packing: **data means pass in the args in order (example: data[0] to quantity, data[1] to next_var, data[2], to next_var_2
        item = ItemModel(name, **data)

        try:
            # Create or update
            item.save_to_db()
        except:
            # 500 indicates a server-side error (example: database problem)
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.quantity = data['quantity']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()
        # The functions will return 200 by default
        return item.json()


class ItemList(Resource):
    def get(self):
        # This style pythonic using list comprehension
        return {'items' : [item.json() for item in ItemModel.query.all()]}
        # This style is for non-python pure style
        #return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
