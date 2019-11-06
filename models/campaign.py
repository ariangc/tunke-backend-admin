from app import db
from models.utils import AddUpdateDelete

class Campaign(db.Model, AddUpdateDelete):
    __tablename__ = 'campaign'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    month = db.Column(db.String(255))
    startDate = db.Column(db.DateTime)
    endDate = db.Column(db.DateTime)
    minimumLoan = db.Column(db.Integer)
    maximumLoan = db.Column(db.Integer)
    minimumPeriod = db.Column(db.Integer)
    maximumPeriod = db.Column(db.Integer)
    interestRate = db.Column(db.Integer)
    idCurrency = db.Column('idCurrency', db.ForeignKey('currency.id'))
    leads = db.relationship('Lead')
    loans = db.relationship('Loan')
    active = db.Column(db.Integer)

    def toJson(self):
        d = {}
        d['idCampaign'] = self.id
        d['name'] = self.name
        d['month'] = self.month
        d['startDate'] = self.startDate.strftime('%d-%m-%Y')
        d['endDate'] = self.endDate.strftime('%d-%m-%Y')
        d['minimumLoan'] = self.minimumLoan
        d['maximumLoan'] = self.maximumLoan
        d['minimumPeriod'] = self.minimumPeriod
        d['maximumPeriod'] = self.maximumPeriod
        d['interestRate'] = self.interestRate
        d['idCurrency'] = self.idCurrency
        d['active'] = self.active
        return d