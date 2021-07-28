from main import db

class User(db.Model):
    __tablename__ = "User"
    UserID = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    password = db.Column(db.String)

db.create_all()

