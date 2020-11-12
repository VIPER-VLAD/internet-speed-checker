import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


class GoogleSheet:
	__scopes = ['https://www.googleapis.com/auth/spreadsheets']

	def __init__(self, sheet_id: str, range_name: str) -> None:
		current_dir = os.path.dirname(os.path.realpath(__file__))

		self.__sheet_id = sheet_id
		self.__value_input_option = 'USER_ENTERED'
		self.__auth_file = current_dir + '/google-sheet-auth.json'
		self.__token_file = current_dir + '/token.pickle'
		self.__range_name = range_name
		self.__auth()
		super().__init__()

	def __auth(self):
		creds = None

		if os.path.exists(self.__token_file):
			with open(self.__token_file, 'rb') as token:
				creds = pickle.load(token)

		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(self.__auth_file, self.__scopes)
				creds = flow.run_local_server(port=0)
			with open(self.__token_file, 'wb') as token:
				pickle.dump(creds, token)

		self.__service = build('sheets', 'v4', credentials=creds).spreadsheets()

	def append(self, values: dict):
		body = {
			'values': values
		}

		self.__service.values().append(
			spreadsheetId=self.__sheet_id,
			valueInputOption=self.__value_input_option,
			range=self.__range_name,
			body=body
		).execute()
