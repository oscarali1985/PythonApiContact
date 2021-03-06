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
            "full_name" not in new_contacto or
            "email" not in new_contacto or
            "address"  not in new_contacto or
            "phone" not in new_contacto
            ):
            return jsonify({
                "resultado" : "Favor revise que este suministrando todos los campos requeridos ingresadas"
            }), 400
        if(
            new_contacto["full_name"] == "" or
            new_contacto["email"] == "" or
            new_contacto["address"]  == "" or
            new_contacto["phone"] == ""
            ):
            return jsonify({
                "resultado" : "Favor revise los valores ingresados"
            }), 400
        new_contacto = Contact.add(
            new_contacto["full_name"],
            new_contacto["email"],
            new_contacto["address"],
            new_contacto["phone"]
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
    "PATCH": devuelve una lista de contacto
    """
    contactoUpdate = Contact.query.get(contact_id)
    if isinstance(contactoUpdate, Contact):
        if request.method == "PATCH":
            valid = 3
            diccionario = request.get_json()
            print(diccionario)
            contactoUpdate.update_contact(diccionario)

            groupd = diccionario["group"]
            print(groupd)
            getGroup = Group.query.get(groupd)
            print(getGroup)
            if (getGroup == None):
                print(getGroup)
                
                
            else:
                #Se verifica si existe el registro en el contacto
                groupreg = contactoUpdate.SusExist()
                
                for x, y in groupreg.items():
                    
                    for a in y:
                        print(a['group_id'])
                        if (str(a['group_id']) == str(groupd)):
                            valid = 1
                            break
                        else:
                            valid = 0

                
            # print("If valid")
            # if (valid == True):
            #     # se debe configurar para que se elimine
            #     print(valid)
                
                
            if (valid == 0):
                print(valid)
                new_suscription = Suscripcion(contact_id, groupd)
                #getSus =Suscripcion.query.get(group)
                #getg =Suscripcion.query.get(getSus)
                #print(getg)
                #print (getSus)
                db.session.add(new_suscription)
            
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

@app.route('/contact/<int:contact_id>', methods = ["DELETE", "POST", "PUT"])

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



#
# Group 
#
@app.route('/group/all', methods=["GET", "POST", "PUT"])

def getAllGroup():
    """
    "GET": devuelve una lista de todos los grupo
    """

    if request.method == "GET":
        groups = Group.query.all()
        groups_serializados = list(map(lambda groupa: groupa.serialize(), groups))
        return jsonify(groups_serializados), 200
        # contactos = Contact.query.all()
        # contactos_serializados = list(map(lambda contact: contact.serialize(), contactos))
        # return jsonify(contactos_serializados), 200
    else:
        response_body = {
            "msj":"Metodo invalido para este que request"
        }
        return jsonify(response_body), 400

@app.route('/group/<int:cont>', methods=["GET", "POST", "PUT"])

def getOneGroup(cont):
    print(cont)
    """
    "GET": devuelve una lista de un donante
    """

    if request.method == "GET":
        groupF = Group.query.filter(Group.id == cont)
        grupos_serializados = list(map(lambda grouposf: grouposf.serialize2(), groupF))

        if grupos_serializados == []:
            msj="no se encontro el grupo ingresado"
            return jsonify(msj), 200
        else:
            return jsonify(grupos_serializados), 200
    else:
        response_body = {
            "msj":"Metodo invalido para este que request"
        }
        return jsonify(response_body), 400



@app.route('/group/', methods=["GET", "POST", "PUT"])

def addGroup():
    """
    "POST": se agreaga un  contacto a la DB
    """

    if request.method == "POST":
        new_group = request.json
        if new_group is None:
            return jsonify({
                "resultado" : "Favor ingrese los datos del contacto"
            }), 400
        if(
            "group_name" not in new_group
            ):
            return jsonify({
                "resultado" : "Favor revise que este suministrando todos los campos requeridos ingresadas"
            }), 400
        if(
            new_group["group_name"] == ""
            ):
            return jsonify({
                "resultado" : "Favor revise los valores ingresados"
            }), 400
        new_group = Group.addGroup(
            new_group["group_name"]
        )
        db.session.add(new_group)
        try:
            db.session.commit()
            return jsonify(new_group.serialize()),201
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

@app.route('/group/<int:group_id>', methods=["PATCH", "GET", "POST", "PUT"])

def updateGroup(group_id):
    """
    "PATCH": devuelve una lista de un donante
    """
    groupUpdate = Group.query.get(group_id)
    if isinstance(groupUpdate, Group):
        if request.method == "PATCH":
            diccionario = request.get_json()
            groupUpdate.update_group(diccionario)
            try:
                db.session.commit()
                return jsonify(groupUpdate.serialize()),200
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

@app.route('/group/<int:group_id>', methods = ["DELETE", "POST", "PUT"])

def deleteGroup(group_id):
    """
    "DELETE": Elimina el contacto ingresado
    """
    if request.method == "DELETE":
        grupos = Group.query.filter(Group.id == group_id)
        grupos_serializados = list(map(lambda gruposf: gruposf.serialize(), grupos))

        if grupos_serializados == []:
            msj="no se encontro el contacto ingresado"
            return jsonify(msj), 200
        else:
            # remover el donante específico de la sesión de base de datos
            DeleteGroup = Group.query.get(group_id)
            db.session.delete(DeleteGroup)
            # hacer commit y devolver 204
            try:
                db.session.commit()
                msj = "Se ha eliminado el grupo"
                return jsonify({
                "Grupo Eliminado": grupos_serializados
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


#
# Suscripcion 
#

@app.route('/sub/all', methods=["GET", "POST", "PUT"])

def getAllSub():
    """
    "GET": devuelve una lista de todos los grupo
    """

    if request.method == "GET":
        suscrip = Suscripcion.query.all()
        suscrip_serializados = list(map(lambda sus: sus.serialize(), suscrip))
        return jsonify(suscrip_serializados), 200
    else:
        response_body = {
            "msj":"Metodo invalido para este que request"
        }
        return jsonify(response_body), 400



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='127.0.0.1', port=PORT, debug=True)
