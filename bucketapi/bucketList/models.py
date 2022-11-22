from bucketList import db
import hashlib


class ExtraMin(object):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Bucketitems(db.Model , ExtraMin):
    """This class represents the bucketlist table."""

    __tablename__ = 'bucketlist'

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def get_by_user(cls, user_id):
        return cls.query.filter_by(created_by=user_id).all()
    
    
class User(db.Model , ExtraMin):
    """This class represents the users table."""
    __tablename__ = 'users'
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    
    
    @staticmethod
    def hash_password(password ):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password, hash):
        return hash == hashlib.sha256(password.encode()).hexdigest()
    
    @classmethod
    def get_users(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    

