from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

# The users table for the db
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)
    """Time to initialize relationship"""
    recipes = db.relationship('Recipe', back_populates="user", cascade='all, delete-orphan') # Assigning users their recepies    

    def __repr__(self):
        return f'<User {self.username}, ID {self.id}>'
    
    """Time to make this password to be stored securely to
    avoid sensitive data to be leaked"""
    @hybrid_property
    def password_hash(self):
        return self._password_hash
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))

        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.endcode('utf-8'))

# The recepie table for the db
class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, db.CheckConstraint('len(instructions) >= 50'))
    minutes_to_complete = db.Column(db.Integer)
    """Adding a foerign key to connect the user table to the recpie table"""
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # Connection gained
    """Acquriring relationship between the two tables which are users and recipes"""
    user = db.relationship('User', back_populates="recipes") # Assigning a user to their recpective recepies