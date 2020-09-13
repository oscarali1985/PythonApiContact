from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#
# Contact 
#

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(250), unique=False)
    phone = db.Column(db.String(50), unique=False)
    
    suscripciones = db.relationship("Suscripcion", backref="contact")

    def __init__(self, full_name, email, address, phone):
        self.full_name = full_name
        self.email = email
        self.address = address
        self.phone = phone
        
    @classmethod
    def add(cls, full_name, email, address, phone):
        """
        Se normaliza el registro de la clase
        """
        new_contact = cls(
            full_name,
            email.lower().capitalize(),
            address,
            phone,
        )
        return new_contact

    def __repr__(self):
        return '<Contact %r>' % self.full_name

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "address" : self.address,
            "phone": self.phone,
            "suscripciones": [suscripcion.serializeG() for suscripcion in self.suscripciones]
            # do not serialize the password, its a security breach
        }

    def update_contact(self, diccionario):
        """ Actualiza el contacto        """
        if "full_name" in diccionario:
            self.full_name = diccionario["full_name"]
        if "email" in diccionario:
            self.email = diccionario["email"]
        if "address" in diccionario:
            self.address = diccionario["address"]
        if "phone" in diccionario:
            self.phone = diccionario["phone"]
        if "suscripciones" in diccionario:
            self.suscripciones = diccionario["suscripciones"]
        return True

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100), unique=True, nullable=False)
    
    suscripciones = db.relationship("Suscripcion", backref="group")

    def __init__(self, group_name):

        self.group_name = group_name

    @classmethod
    def addGroup(cls, group_name):
        """
        Se normaliza el registro de los grupo
        """
        addG = cls(
            group_name.lower().capitalize()
        )
        return addG


    def __repr__(self):
        return '<Group %r>' % self.group_name

    def serialize(self):
        return {
            "id": self.id,
            "group_name": self.group_name,
            #"Miembros" : [suscripcion.serialize() for suscripcion in self.suscripciones]
        }

    def serialize2(self):
        return {
            "id": self.id,
            "group_name": self.group_name,
            "Miembros" : [suscripcion.serializeC() for suscripcion in self.suscripciones]
        }    

    def update_group(self, diccionario):
        """ Actualiza el contacto        """
        if "group_name" in diccionario:
            self.group_name = diccionario["group_name"]
        
        return True

class Suscripcion(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __init__(self, contact_id, group_id):
        self.contact_id = contact_id
        self.group_id = group_id

    def __repr__(self):
        return '<Suscripcion %r>' % self.group_id

    def serialize(self):
        return {
            #"id": self.id,
            "group_id" : self.group.id,
            "contact_id": self.contact.id
        }

    def serializeC(self):
        return {
            #"id": self.id,
            #"group_id" : self.group.id,
            "contact_id": self.contact.id
        }

    def serializeG(self):
        grupo = []
        grupo.append(self)
        print(grupo)
        return {
            #"id": self.id,
            #"group_id" : grupo,
            #"contact_id": self.contact.id
        }

