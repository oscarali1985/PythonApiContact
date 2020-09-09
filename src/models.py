from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(250), unique=False)
    phone = db.Column(db.String(50), unique=False)
    
    suscripcion = db.relationship("Suscripcion", backref="Contact")

    def __init__(self, full_name, email, address, phone):
        self.full_name = full_name
        self.email = email
        self.address = address
        self.phone = phone
        

    def __repr__(self):
        return '<Contact %r>' % self.full_name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "address" : self.address,
            "phone": self.phone,
            'suscripciones': [suscripcion.serialize() for suscripcion in self.group.group_name],
            # do not serialize the password, its a security breach
        }

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100), unique=True, nullable=False)
    
    suscripcion = db.relationship("Suscripcion", backref="Group")

    def __init__(self, id,group_name):
        self.id = id
        self.group_name = group_name

    def __repr__(self):
        return '<Group %r>' % self.group_name

    def serialize(self):
        return {
            "id": self.id,
            "group_name": self.group_name,
            "Miembros" : [suscripcion.serialize() for suscripcion in self.contact.full_name],
        }

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
            "id": self.id,

            "group_name" : self.group.group_name,
            "contact_name": self.contact.full_name
        }