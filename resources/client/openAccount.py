from datetime import datetime, timedelta
from models.prospectiveClient import ProspectiveClient
from models.account import Account 
from models.additionalQuestion import AdditionalQuestion
from models.accountType import AccountType
from models.person import Person 
from models.client import Client
from resources.utils import GenerateAccount
from models.salesRecord import SalesRecord
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
import status
from flask import request, render_template
from flask_mail import Message
from app import db

class OpenAccountResource(Resource):
	def post(self):
		requestDict = request.get_json()
		if not requestDict:
			response = {'error': 'No input data provided'}
			return response, status.HTTP_400_BAD_REQUEST
		curdatetime = datetime.now() - timedelta(hours=5)
		try:
			accountType = 1 #Cuenta Simple por defecto
			if 'accountType' in requestDict:
				accountType = int(requestDict['accountType'])
			idPerson = requestDict['idPerson']
			origin = requestDict['origin']
			prospectiveClient = ProspectiveClient.query.filter_by(idPerson=idPerson).first()
			client = Client.query.filter_by(idProspectiveClient=prospectiveClient.id).first()
			if not client: #Apertura de cuentas no cliente
				client = Client(registerDate=curdatetime, totalAccounts=1, activeLoans=0, active=1, idProspectiveClient=prospectiveClient.id)
				client.add(client)
			else:
				client.totalAccounts += 1
				client.update()
			db.session.flush()
			orig = ""
			if origin==1:
				orig = "Web"
			else:
				orig = "Ventanilla" 
			salesRecord = SalesRecord(origin=orig, active=1,requestDate=curdatetime,idClient=client.id, idRecordStatus=1, idProduct=1)
			salesRecord.add(salesRecord)
			db.session.flush()
			currency = requestDict['currency']
			account = Account(accountNumber=GenerateAccount(), balance=0.0, openingDate=curdatetime, 
							closingDate=None, cardNumber="1234-5678-1234-5678", idAccountType=accountType,
							idSalesRecord=salesRecord.id, idCurrency=currency, idClient=client.id, active=1)
			account.add(account)
			db.session.flush()
			response1 = requestDict['response1']
			response2 = requestDict['response2']
			response3 = requestDict['response3']
			response4 = requestDict['response4']
			additionalQuestion = AdditionalQuestion(
				response1=response1,
				response2=response2,
				response3=response3,
				response4=response4,
				idAccount=account.id
			)
			additionalQuestion.add(additionalQuestion)

			#Commit changes
			db.session.commit()

			regClient = Client.query.get(client.id)
			regAccount = Account.query.get(account.id)
			regAccountType = AccountType.query.get(accountType)
			person = Person.query.get(prospectiveClient.idPerson)
			d = {}
			d['name'] = " ".join([person.firstName, person.middleName, person.fatherLastname, person.motherLastname])
			d['accountNumber'] = regAccount.accountNumber
			d['cci'] = "0011-" + regAccount.accountNumber
			d['accountDetail'] = regAccountType.typeName
			d['openingDate'] = regAccount.openingDate.strftime('%d-%m-%Y')
			d['currency'] = ('Soles' if regAccount.idCurrency == 1 else 'Dolares')
			d['email'] = prospectiveClient.email1

			from mailing import mail
			msg = Message("Tunke - Apertura de cuenta exitosa", sender="tunkestaff@gmail.com", recipients=[d['email']])
			msg.body = 'Hola'
			msg.html = render_template('ejemplo.html', name=d['name'], accountNumber=d['accountNumber'], cci=d['cci'], accountDetail=d['accountDetail'],
										openingDate=d['openingDate'], currency=d['currency'])
			mail.send(msg)
			return d, status.HTTP_201_CREATED

		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST
		except Exception as e:
			db.session.rollback()
			response = {'error': 'An error ocurred. Contact cat-support asap. ' + str(e)}
			return response, status.HTTP_400_BAD_REQUEST
