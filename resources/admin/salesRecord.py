from app import db
from resources.admin.security import AuthRequiredResource
from models.salesRecord import SalesRecord
from models.recordStatus import RecordStatus
from models.client import Client
from models.product import Product
from models.prospectiveClient import ProspectiveClient
from models.person import Person
from models.account import Account
from models.loan import Loan
from models.bankAccount import BankAccount
from models.transaction import Transaction
from models.share import Share
from models.currency import Currency
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from flask import request, render_template
import status
from datetime import datetime, timedelta
import requests, json
from flask_mail import Message
import pdfkit

class SalesRecordListResource(AuthRequiredResource):
    def get(self):
        try:
            salesRecords = SalesRecord.query.all()
            d = {}
            d['salesRecords'] = []
            for salesRecord in salesRecords:
                salesRecord = salesRecord.toJson()
                recordStatus = RecordStatus.query.get_or_404(salesRecord['idRecordStatus'])
                client = Client.query.get_or_404(salesRecord['idClient'])
                product = Product.query.get_or_404(salesRecord['idProduct'])
                client = client.toJson()
                prospectiveClient = ProspectiveClient.query.get_or_404(client['idProspectiveClient'])
                prospectiveClient = prospectiveClient.toJson()
                person = Person.query.get_or_404(prospectiveClient['idPerson'])
                e = {}
                if salesRecord['idProduct']==1:
                    account = Account.query.filter_by(idSalesRecord=salesRecord['idSalesRecord']).first()
                    account = account.toJson()
                    e['activeAccount'] = account['active']
                    e['balance'] = account['balance']
                    e['openingDate'] = account['openingDate']
                    e['closingDate'] = account['closingDate']
                    e['accountNumber'] = account['accountNumber']
                else:
                    loan = Loan.query.filter_by(idSalesRecord=salesRecord['idSalesRecord']).first()
                    loan = loan.toJson()
                    e['amount'] = loan['amount']
                    e['activeLoan'] = loan['active']
                    e['totalShares'] = loan['totalShares']
                    e['idLoan'] = loan['idLoan']
                    e['interestRate'] = loan['interestRate']
                    e['idLead'] = loan['idLead']
                    if loan['idShareType']==1:
                        e['shareType'] = 'Ordinaria'
                    else:
                        e['shareType'] = 'Extraordinaria'
                person = person.toJson()
                product = product.toJson()
                recordStatus = recordStatus.toJson()
                nationality = json.loads(requests.get('https://restcountries.eu/rest/v2/alpha/' + person['nationality']).text)
                e['nationality'] = nationality['name']
                e['flag'] = nationality['flag']
                e['activeClient'] = client['active']
                e['nameRecordStatus'] = recordStatus['name']
                e['firstName'] = person['firstName']
                e['middleName'] = person['middleName']
                e['fatherLastname'] = person['fatherLastname']
                e['motherLastname'] = person['motherLastname']
                e['birthdate'] = person['birthdate']
                e['address'] = person['address']
                e['documentType'] = person['documentType']
                e['documentNumber'] = person['documentNumber']
                e['idSalesRecord'] = salesRecord['idSalesRecord']
                e['origin'] = salesRecord['origin']
                e['requestDate'] = salesRecord['requestDate']
                e['activeSalesRecord'] = salesRecord['active']
                e['productName'] = product['name']
                d['salesRecords'].append(e)
            return d, status.HTTP_200_OK

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error':str(e)}
            return response, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            db.session.rollback()
            response = {'error':str(e)}
            return response, status.HTTP_400_BAD_REQUEST


class SalesRecordResource(AuthRequiredResource):

    	def put(self,id):
            try:
                requestDict = request.get_json()
                if not requestDict:
                    response = {'error': 'No input data provided'}
                    return response, status.HTTP_400_BAD_REQUEST

                state = requestDict['state']

                salesRecord = SalesRecord.query.get_or_404(id)
                loan = Loan.query.filter_by(idSalesRecord=id).first()
                loan = loan.toJson()
                account = Account.query.get_or_404(loan['idAccount'])
                currency = Currency.query.get_or_404(account.idCurrency)
                currency = currency.toJson()
                aux = account.toJson()
                client = Client.query.get_or_404(loan['idClient'])
                prospectiveClient = ProspectiveClient.query.get_or_404(client.idProspectiveClient)
                bankAccount = BankAccount.query.get_or_404(aux['idCurrency'])
                if state == 1:#aprobado
                    salesRecord.idRecordStatus = 1
                    salesRecord.requestDate = datetime.now() - timedelta(hours=5)
                    account.balance = account.balance + loan['amount']
                    bankAccount.balance = bankAccount.balance - loan['amount']
                    bankAccount.update()
                    transaction = Transaction(datetime=datetime.now() - timedelta(hours=5),amount=loan['amount'],idAccount=loan['idAccount'],idBankAccount=aux['idCurrency'],active=1)
                    transaction.add(transaction)
                    client.activeLoans = 0
                elif state == 2:
                    salesRecord.idRecordStatus = 2
                    salesRecord.requestDate = datetime.now() - timedelta(hours=5)
                    client.activeLoans = 0

                salesRecord.update()
                client.update()
                account.update()
                db.session.commit()
                response = {'ok': 'Prestamo actualizado satisfactoriamente.'}

                from mailing import mail

                if state==1:
                    msg = Message("Tunke - Prestamo aprobado", sender="tunkestaff@gmail.com", recipients=[prospectiveClient.email1])
                    msg.body = 'Enhorabuena, tu prestamo fue aprobado'
                    sharesA = Share.query.filter_by(idLoan=loan['idLoan'])
                    shares = []
                    totalAmortization = 0
                    totalInterest = 0
                    totalComission = 0
                    totalShare = 0
                    for sha in sharesA:
                        e = sha.toJson()
                        shares.append(e)
                        totalAmortization+=e['amortization']
                        totalInterest+=e['interest']
                        totalComission+=e['commission']
                        totalShare+=e['feeAmount']
                    currencySymbol = currency['currencySymbol']
                    rendered = render_template('calendar.html', shares=shares, currencySymbol=currencySymbol,totalAmortization=str(round(totalAmortization, 2)),totalInterest=str(round(totalInterest,2)),totalComission=str(round(totalComission,2)),totalShare=str(round(totalShare,2)))
                    pdf = pdfkit.from_string(rendered , False)
                    msg.attach("Calendario.pdf","application/pdf",pdf)
                elif state==2:
                    msg = Message("Tunke - Prestamo rechazado", sender="tunkestaff@gmail.com", recipients=[prospectiveClient.email1])
                    msg.body = 'Lo sentimos, tu prestamo fue rechazado. Acercarse a las oficinas para mas informacion'
                mail.send(msg)	
                return response, status.HTTP_200_OK

            except SQLAlchemyError as e:
                db.session.rollback()
                response = {'error': str(e)}
                print(e)
                return response, status.HTTP_400_BAD_REQUEST

            except Exception as e:
                db.session.rollback()
                response = {'error': str(e)}
                print(e)
                return response, status.HTTP_400_BAD_REQUEST

