from flask import Blueprint
from flask_restful import Api, Resource

# Importing Resources from resources/
from resources.admin.user import UserListResource, UserResource
from resources.admin.authentication import LoginResource
from resources.admin.authentication import SignupResource
from resources.admin.person import PersonListResource, PersonResource, PersonDocumentResource
from resources.admin.client import ClientListResource, ClientResource
from resources.admin.account import AccountListResource, AccountResource 
from resources.admin.authentication import VerifyEmailResource
from resources.client.dniValidation import DniValidationResource
from resources.admin.account import GetByClientResource
from resources.admin.parameterSettings import ParameterSettingsResource
from resources.admin.salesRecord import SalesRecordListResource,SalesRecordResource
from resources.admin.campaign import CampaignResource, CampaignListResource, CampaignChargeResource
from resources.admin.loan import LoanResource, LoanListResource
from resources.admin.blackList import BlackListListResource, BlackListResource
from resources.admin.bankAccount import BankAccountResource
from resources.admin.transaction import TransactionListResource
from resources.admin.lead import LeadListResource, GetByCampaignResource
from resources.admin.share import ShareListResource
from resources.admin.account import GetByNationality
from resources.admin.account import GetByPeriod
from resources.admin.loan import GenerateCalendarResource
from resources.admin.authentication import LogoutResource

apiBp = Blueprint('api', __name__)
api = Api(apiBp)

api.add_resource(UserResource, '/users/<int:id>')
api.add_resource(UserListResource, '/users/')
api.add_resource(SignupResource, '/signup')
api.add_resource(LoginResource, '/login')
api.add_resource(PersonResource, '/persons/<int:id>')
api.add_resource(PersonListResource, '/persons/')
api.add_resource(ClientResource, '/clients/<int:id>')
api.add_resource(ClientListResource, '/clients/')
api.add_resource(AccountResource, '/accounts/<int:id>')
api.add_resource(AccountListResource, '/accounts/')
api.add_resource(VerifyEmailResource, '/verifyEmail/')
api.add_resource(PersonDocumentResource, '/persons/getByDocument/')
api.add_resource(DniValidationResource, '/dniValidation/')
api.add_resource(GetByClientResource, '/accounts/getByClient/')
api.add_resource(ParameterSettingsResource, '/parameterSettings/')
api.add_resource(SalesRecordResource,'/salesRecord/<int:id>')
api.add_resource(SalesRecordListResource,'/salesRecords/')
api.add_resource(CampaignResource,'/campaign/<int:id>')
api.add_resource(CampaignListResource,'/campaigns/')
api.add_resource(LoanResource,'/loan/<int:id>')
api.add_resource(LoanListResource, '/loans/')
api.add_resource(BankAccountResource,'/bankAccount/')
api.add_resource(BlackListListResource,'/blackLists/')
api.add_resource(TransactionListResource,'/transactions/')
api.add_resource(CampaignChargeResource,'/campaignCharge/')
api.add_resource(LeadListResource,'/leads/')
api.add_resource(BlackListResource,'/blackList/')
api.add_resource(GetByCampaignResource,'/leads/getByCampaign/')
api.add_resource(ShareListResource,'/shares/')
api.add_resource(GetByNationality,'/accounts/getByNationality/')
api.add_resource(GetByPeriod,'/accounts/getByPeriod/')
api.add_resource(LogoutResource, '/logoff/')
api.add_resource(GenerateCalendarResource, '/loans/generateCalendar/')