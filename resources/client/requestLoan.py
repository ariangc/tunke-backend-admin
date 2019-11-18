from app import db
from models.loan import Loan
from models.client import Client
from models.salesRecord import SalesRecord
from models.bankAccount import BankAccount
from models.campaign import Campaign
from models.currency import Currency
from models.person import Person
from models.prospectiveClient import ProspectiveClient
from models.account import Account
from models.transaction import Transaction
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from flask import request, render_template
from flask_mail import Message
import status
import pdfkit

class RequestLoanResource(Resource):
	def post(self):
		try:
			requestDict = request.get_json()
			if not requestDict:
				response = {'error': 'No input data provided'}
				return response, status.HTTP_400_BAD_REQUEST

			idClient = int(requestDict['idClient'])
			totalShares = int(requestDict['totalShares'])
			amount = float(requestDict['amount'])
			interestRate = float(requestDict['interestRate'])
			idCampaign = int(requestDict['idCampaign'])
			idShareType = int(requestDict['idShareType'])
			share = float(requestDict['share'])
			idAccount = int(requestDict['idAccount'])
			commission = float(requestDict['commission'])
			#Obteniendo campaign
			campaign = Campaign.query.get_or_404(idCampaign)

			#Minus en bank account
			bankAccount = BankAccount.query.get_or_404(campaign.idCurrency)
			bankAccount.balance = bankAccount.balance - amount
			bankAccount.update()

			#Plus in AccountClient
			account = Account.query.get_or_404(idAccount)
			account.balance = account.balance + amount
			account.update()
			
			#Update boolean in client
			client = Client.query.get_or_404(idClient)
			if client.activeLoans==1:
				response = {'error': 'El cliente tiene un préstamo activo'}
				return response, status.HTTP_400_BAD_REQUEST
			client.activeLoans = 1
			client.update()

			#Insert in salesRecord
			salesRecord = SalesRecord(origin='Web',requestDate=datetime.now(),idRecordStatus=1,
			active=1,idClient=idClient,idProduct=2)
			salesRecord.add(salesRecord)
			db.session.flush()

			#Insert in loan			
			loan = Loan(totalShares=totalShares,amount=amount,interestRate=interestRate,idCampaign=idCampaign,
			idClient=idClient,idSalesRecord=salesRecord.id,idShareType=idShareType,active=1,idAccount=idAccount,share=share,commission=commission)
			loan.add(loan)
			
			#Insert in transaction
			transaction = Transaction(datetime=datetime.now(),amount=amount,idAccount=idAccount,idBankAccount=campaign.idCurrency,active=1)
			transaction.add(transaction)
			
			#Commit changes
			db.session.commit()

			regLoan = Loan.query.get(loan.id)
			d={}
			d['idLoan'] = str(regLoan.id)
			d['totalShares'] = str(regLoan.totalShares)
			d['amount'] = str(regLoan.amount)
			d['interestRate'] = str(regLoan.interestRate)
			d['idCampaign'] = str(regLoan.idCampaign)
			d['idClient'] = str(regLoan.idClient)
			d['idSalesRecord'] = str(regLoan.idSalesRecord)
			d['idShareType'] = str(regLoan.idShareType)
			d['active'] = str(regLoan.active)
			prospectiveClient = ProspectiveClient.query.get_or_404(client.idProspectiveClient)
			person = Person.query.get_or_404(prospectiveClient.idPerson)
			currency = Currency.query.get_or_404(campaign.idCurrency)

			from mailing import mail
			msg = Message("Tunke - Prestamo exitoso", sender="tunkestaff@gmail.com", recipients=[prospectiveClient.email1])
			msg.body = 'Hola'
			fullName = person.firstName + ' ' + person.fatherLastname
			accNumber = str(account.accountNumber)
			curName = str(currency.currencyName)
			amount = str(d['amount'])
			msg.html = render_template('loans.html', name=fullName, accountNumber=accNumber, currency=curName, amount=amount)
			#rendered = render_template('calendar.html',shares=shares,currencySymbol=currencySymbol,totalAmortization=totalAmortization,totalInterest=totalInterest,totalComission=totalComission,totalShare=totalShare)
			#pdf = pdfkit.from_string(rendered ,False)
			#msg.attach("Calendario.pdf","application/pdf",pdf)
			mail.send(msg)	
			return d, status.HTTP_201_CREATED

		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST

		except Exception as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST