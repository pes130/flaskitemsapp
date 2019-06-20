from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


# Con FlaskRestful no necesitas jsonify porque lo hace el sólo.
class Item(Resource):
    
    # Pertenece a la clase
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item requires a store id"
    )
    
    # Permitimos que el recursos sea accedido por GET
    @jwt_required()
    def get(self, name):   
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400 #Bad request 
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting item. "}, 500
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'Item deleted'}

    # Ojo que en teoría, PUT puede servir para crear y actualizar
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.save_to_db()
        return item.json()
  

class ItemsList(Resource):
    def get(self):
        # Literalmente, haces primero el for, y luego aplicas el item.json a cada uno
        return {'items': [item.json() for item in ItemModel.query.all()]}