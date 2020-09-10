"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Contact, Group, Suscripcion
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)



# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#
# Contact 
#


@app.route('/contact/all', methods=["GET", "POST", "PUT"])

def getAllContact():
    """
    "GET": devuelve una lista de todos los donantes
    """

    if request.method == "GET":
        contactos = Contact.query.all()
        contactos_serializados = list(map(lambda contact: contact.serialize(), contactos))
        return jsonify(contactos_serializados), 200
    else:
        response_body = {
            "msj":"Metodo invalido para este que request"
        }
        return jsonify(response_body), 400

@app.route('/contact/<int:cont>', methods=["GET", "POST", "PUT"])

def getOneContact(cont):
    print(cont)
    """
    "GET": devuelve una lista de un donante
    """

    if request.method == "GET":
        contactos = Contact.query.filter(Contact.id == cont)
        contactos_serializados = list(map(lambda contact: contact.serialize(), contactos))

        if contactos_serializados == []:
            msj="no se encontro el contacto ingresado"
            return jsonify(msj), 200
        else:
            return jsonify(contactos_serializados), 200
    else:
        response_body = {
            "msj":"Metodo invalido para este que request"
        }
        return jsonify(response_body), 400



@app.route('/contact/', methods=["GET", "POST", "PUT"])

def addContact():
    """
    "POST": se agreaga un  contacto a la DB
    """

    if request.method == "POST":
        new_contacto = request.json
        if new_contacto is None:
            return jsonify({
                "resultado" : "Favor ingrese los datos del contacto"
            }), 400
        if(
            "email" not in new_contacto or
            "full_name" not in new_contacto or
            "address"  not in new_contacto or
            "phone" not in new_contacto
            ):
            return jsonify({
                "resultado" : "Favor revise que este suministrando todos los campos requeridos ingresadas"
            }), 400
        if(
            new_contacto["email"] == "" or
            new_contacto["full_name"] == "" or
            new_contacto["address"]  == "" or
            new_contacto["phone"] == ""
            ):
            return jsonify({
                "resultado" : "Favor revise los valores ingresados"
            }), 400
        new_contacto = Contact.add(
            new_contacto["email"],
            new_contacto["full_name"],
            new_contacto["address"],
            new_contacto["phone"],
        )
        db.session.add(new_contacto)
        try:
            db.session.commit()
            return jsonify(new_contacto.serialize()),201
        except Exception as error:
            db.session.rollback()
            return jsonify({
                "resultado": f"{error.args}"
            }),500        
    else:
        response_body = {
            "msj":"Metodo invalido para este que request"
        }
    return jsonify(response_body), 400

@app.route('/contact/<int:contact_id>', methods=["PATCH", "GET", "POST", "PUT"])

def updateContact(contact_id):
    """
    "PATCH": devuelve una lista de un donante
    """
    contactoUpdate = Contact.query.get(contact_id)
    if isinstance(contactoUpdate, Contact):
        if request.method == "PATCH":
            diccionario = request.get_json()
            contactoUpdate.update_contact(diccionario)
            try:
                db.session.commit()
                return jsonify(contactoUpdate.serialize()),200
            except Exception as error:
                db.session.rollback()
                print(f"{error.args} {type(error)}")
                return jsonify({
                    "resultado": f"{error.args}"
                }), 500
        
        else:
            response_body = {
            "msj":"Metodo invalido para este que request"
            }
            return jsonify(response_body), 400

    else:
        # el donante no existe!
        return jsonify({
            "resultado": "el contacto no existe..."
        }), 404

@app.route('/contact/<int:contact_id>', methods = ["DELETE" ,"POST", "PUT"])

def deleteContact(contact_id):
    """
    "DELETE": Elimina el contacto ingresado
    """
    if request.method == "DELETE":
        contactos = Contact.query.filter(Contact.id == contact_id)
        contactos_serializados = list(map(lambda contact: contact.serialize(), contactos))

        if contactos_serializados == []:
            msj="no se encontro el contacto ingresado"
            return jsonify(msj), 200
        else:
            # remover el donante específico de la sesión de base de datos
            DeleteContactos = Contact.query.get(contact_id)
            db.session.delete(DeleteContactos)
            # hacer commit y devolver 204
            try:
                db.session.commit()
                msj = "Se ha eliminado el contacto"
                return jsonify({
                "Contacto Eliminado": contactos_serializados
            }), 205
            except Exception as error:
                db.session.rollback()
                print(f"{error.args} {type(error)}")
                return jsonify({
                    "resultado": f"{error.args}"
                }), 500
    else:
        response_body = {
            "msj":"Metodo invalido para este que request"
        }
        return jsonify(response_body), 400


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='127.0.0.1', port=PORT, debug=True)
