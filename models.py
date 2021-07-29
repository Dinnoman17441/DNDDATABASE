from main import db

class User(db.Model):
    __tablename__ = "User"
    UserID = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    password = db.Column(db.String)

class Spell(db.Model):
    __tablename__ = "Spell"
    SpellID = db.Column(db.Integer, primary_key = True)
    SpellName = db.Column(db.String)
    SpellLevel = db.Column(db.Integer)
    CastingTime = db.Column(db.String)
    Range = db.Column(db.String)
    Components = db.Column(db.String)
    Duration = db.Column(db.String)
    Description = db.Column(db.String)

    OwnerID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    SchoolID = db.Column(db.Integer, db.ForeignKey('School.SchoolID'), nullable=False)
    SourceID = db.Column(db.Integer, db.ForeignKey('Source.SourceID'), nullable=False)

    owner = db.relationship("User", backref="spells")
    school = db.relationship("School", backref="spells")
    source = db.relationship("Source", backref="spells")

class Item(db.Model):
    __tablename__ = "Item"
    ItemID = db.Column(db.Integer, primary_key = True)
    ItemName = db.Column(db.String)
    Description = db.Column(db.String)
    ItemType = db.Column(db.String)
    ItemRarity = db.Column(db.String)

    OwnerID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    SourceID = db.Column(db.Integer, db.ForeignKey('Source.SourceID'), nullable=False)

    owner = db.relationship("User", backref="items")
    source = db.relationship("Source", backref="items")

class School(db.Model):
    __tablename__ = "School"
    SchoolID = db.Column(db.Integer, primary_key = True)
    SchoolName = db.Column(db.String)

class Source(db.Model):
    __tablename__ = "Source"
    SourceID = db.Column(db.Integer, primary_key = True)
    SourceName = db.Column(db.String)

db.create_all()

