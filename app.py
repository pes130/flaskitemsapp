import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemsList
from resources.store import Store, StoreList

# Un resource es como una clase modelo

app = Flask(__name__)
# HEroku me tiene una variable de entorno llamada DATABASE_URL con la cadena de conexión a 
# la base de datos. Así evito poner en el código postgres://...... 
# con el get(cosa1, cosa2). Si cosa1 es undefined, se coge la cosa 2, así puedo ejecutar en local
# usando una bd sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite://data.db')
# Trackear modificaciones en objetos no guardadas. Desactivamos el de 
# SQLAlchemy porque el de Flask-SQLAlchemy es mejor
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



app.secret_key = 'pablo'
# Nos permite asociar facilmente recursos a métodos.
api = Api(app)

# esto te crea un nuevo endpoint /auth
# cuando le llamamos le mandamos un usuario y contraseña
jwt = JWT(app, authenticate, identity)






    

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemsList,'/items')
api.add_resource(UserRegister,'/register')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')


# Ojo con esto, que si importas este fichero, se ejecuta esto. Para evitarlo, línea siguiente
#app.run(port=5000, debug=True)

# Con uWSGI no pasas por aquí, así que no importas db
if __name__ == '__main__':
    # Imports circulares, si importamos db al princpio, y en models también vas a crear una importación circular
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)