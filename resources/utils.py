# Check password strength with Password_Strength module
from password_strength import PasswordPolicy
from random import randint
from twilio.rest import Client
from flask_mail import Message
from credentials import accountSid, authToken, myTwilio

passwordPolicy = PasswordPolicy.from_names(
	length=5,  # min length: 8
	uppercase=1,  # need min. 2 uppercase letters
	numbers=1,  # need min. 2 digits
	special=1,  # need min. 2 special characters
	nonletters=0,  # need min. 2 non-letter characters (digits, specials, anything)
)

documentLenghts = [8, 12, 11, 12, 15, 15]
documentTypes = ["DNI", "CARNET DE EXTRANJERIA", "REG. UNICO DE CONTRIBUYENTES", "PASAPORTE", "PART. NACIMIENTO", "OTROS"]

def GenerateAccount():
	res = ""
	for i in range(14):
		if i == 3 or i == 7:
			res += '-'
			continue
		res += chr(ord('0') + randint(0,9))

	return res

def SendMail(subject, sender, to, msgBody):
	from mailing import mail
	msg = Message(subject, sender=sender, recipients=[to])
	msg.body= msgBody
	mail.send(msg)

def SendSMS(cellphone, msg):
	client = Client(accountSid, authToken)
	message = client.messages.create(to=("+51"+cellphone), from_=myTwilio, body=msg)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['csv', 'xlsx']

def fixDocumentNumber(documentNumber):
	while len(documentNumber) not in documentLenghts:
		documentNumber = "0" + documentNumber
	return documentNumber
		
def getDocumentType(documentNumber):
	for i in range(len(documentLenghts)):
		if len(documentNumber) == documentLenghts[i]:
			return documentTypes[i]
	return documentTypes[0]