import base64
import requests


class Router:
	def __init__(self, url: str, login: str, password: str) -> None:
		self.__url = url.replace(r"\/$", '')
		self.__login = login
		self.__password = password
		self.__generate_auth_cookie()
		super().__init__()

	def __generate_auth_cookie(self):
		auth = self.__login + ':' + self.__password
		token = base64.b64encode(auth.encode()).decode('ascii')

		self.__auth_cookie = 'Authorization=Basic ' + token

	def get_lan_hosts_count(self):
		url = self.__url + '/cgi?5'

		headers = {
			'Referer': self.__url + '/mainFrame.htm',
			'Cookie': self.__auth_cookie,
		}

		request = requests.post(url, headers=headers, data="[LAN_HOST_ENTRY#0,0,0,0,0,0#0,0,0,0,0,0]0,1\r\nhostName\r\n")

		return int(request.text.count("\n") / 2)
