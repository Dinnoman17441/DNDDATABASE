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
    V = db.Column(db.Integer)
    S = db.Column(db.Integer)
    M = db.Column(db.Integer)
    Materials = db.Column(db.String)
    Duration = db.Column(db.String) 
    Description = db.Column(db.String)
    AtHigherLevels = db.Column(db.String)
    Concentration = db.Column(db.Integer)
    Ritual = db.Column(db.Integer)

    OwnerID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    SchoolID = db.Column(db.Integer, db.ForeignKey('School.SchoolID'), nullable=False)
    SourceID = db.Column(db.Integer, db.ForeignKey('Source.SourceID'), nullable=False)

    owner = db.relationship("User", backref="spells")
    school = db.relationship("School", backref="spells")
    source = db.relationship("Source", backref="spells")

class School(db.Model):
    __tablename__ = "School"
    SchoolID = db.Column(db.Integer, primary_key = True)
    SchoolName = db.Column(db.String)

class Source(db.Model):
    __tablename__ = "Source"
    SourceID = db.Column(db.Integer, primary_key = True)
    SourceName = db.Column(db.String)

db.create_all()
#db.session.commit()


'''
#Adds list of Schools to database on formation
ABJ = School(SchoolName = "Abjuration")
CON = School(SchoolName = "Conjuration")
DIV = School(SchoolName = "Divination")
ENC = School(SchoolName = "Enchantment")
EVO = School(SchoolName = "Evocation")
ILL = School(SchoolName = "Illusion")
NEC = School(SchoolName = "Necromancy")
TRA = School(SchoolName = "Transmutation")
OTH = School(SchoolName = "Other")

db.session.add(ABJ)
db.session.add(CON)
db.session.add(DIV)
db.session.add(ENC)
db.session.add(EVO)
db.session.add(ILL)
db.session.add(NEC)
db.session.add(TRA)
db.session.add(OTH)

#Adds list of Sources to database on formation
Official = Source(SourceName = "Official")
Homebrew = Source(SourceName = "Homebrew")

db.session.add(Official)
db.session.add(Homebrew)

db.session.commit()
#'''