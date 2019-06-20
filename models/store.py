from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    # le añadimos id porque es útil
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    items = db.relationship('ItemModel', lazy='dynamic') # Con esto, SQLAlchemy ya se busca solo la vida y busca
    # la relación. Sabe que es una relación uno a muchos y te convierte esto en una lista
    # el lazy es para que cada vez que leas un store, consultes todos sus items en la base de datos

    def __init__(self, name):
        self.name = name
    
    def json(self):
        # devuelves un diccionario
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return StoreModel.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        