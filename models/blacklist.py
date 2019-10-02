from app import db
from models.utils import AddUpdateDelete

class Blacklist(db.Model, AddUpdateDelete):
    __tablename__ = 'blacklist'
    id = db.Column(db.Integer, primary_key=True)
    documentType = db.Column(db.String(100))
    documentNumber = db.Column(db.String(20), unique=True)
    active = db.Column(db.Boolean)
    idBlacklistClassification = db.Column('idBlacklistClassification', db.ForeignKey('blacklistClassification.id'))