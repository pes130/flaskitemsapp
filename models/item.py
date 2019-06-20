from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    # le añadimos id porque es útil
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')
    # Con lo anterior decimos que cada item tiene un store cuyo id es lo que se almacena en store_id
    # También podemos hacer la relacion inversa en stores y lo vamos  a hacer
    

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id
    
    def json(self):
        # devuelves un diccionario
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        # puedes encadenar todos los filter_by que quieras
        # equivale a SELECT * FROM items WHERE name=? LIMIT 1
        print("Vamos a buscar cosas con el name=",name)
        return ItemModel.query.filter_by(name=name).first()

    def save_to_db(self):
        #INSERT INTO items VALUES (?, ?)
        # LO de la sesión son los objetos que tienes en memoria. No tiens que 
        # preocuparte de si es una inserción o un update
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        