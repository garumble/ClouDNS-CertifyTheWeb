import certifi
import json
from urllib3 import PoolManager, util

class WebService(object):
	baseUrl = 'https://api.cloudns.net/dns/'
	authId = '3581'
	authPassword = 'AtQ|m73{j87HKJ~7!'
	log = None

	def __init__(self, config = None, flash = None, workers = None, log = None):
		timeout = util.timeout.Timeout(60)
		self.http = PoolManager(timeout = timeout, cert_reqs = 'CERT_REQUIRED', ca_certs = certifi.where())

	def call(self, queryString, data = None):
		if data:
			response = self.http.request('POST', self.baseUrl + queryString, body = json.dumps(data).encode('utf-8'), headers = {'Content-type': 'application/json', 'Cache-Control': 'No-Cache'})
		else:
			response = self.http.request('GET', self.baseUrl + queryString, headers = {'Content-type': 'application/json', 'Cache-Control': 'No-Cache'})
		# 2xx codes are OK
		if response.status < 200 or response.status >= 300:
			# need to do something here to report
			return None

		# success, but no data
		if response.status == 204:
			return []

		result = json.loads(response.data.decode('utf-8'))
		if 'status' in result:
			if result['status'] == 'Failed':
				# report error
				return None
			else:
				return []
		else:
			return result

	def queryString(self, function, domain):
		return '%s.json?auth-id=%s&auth-password=%s&domain-name=%s' % (function, self.authId, self.authPassword, domain)

	def list(self, domain):
		response = self.call(self.queryString('records', domain))
		return response

	def add(self, domain, key, value):
		add = self.queryString('add-record', domain) + '&record-type=TXT&host=%s&record=%s&ttl=3600' % (key, value)
		self.call(add)

	def delete(self, domain, key):
		response = self.list(domain)
		if response != None:
			delete = self.queryString('delete-record', domain) + '&record-id=%s'
			for r in response:
				entry = response[r]
				if entry['type'] == "TXT" and entry['host'] == key:
					self.call(delete % r)
			return True
		return False
