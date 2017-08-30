#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from urllib.parse import urlencode as _urlencode

from decimal import Decimal
from json import loads as _loads
from hmac import new as _new
from hashlib import sha512 as _sha512
from time import time, sleep
# 3rd party
#from requests.exceptions import RequestException
from requests import get as _get


PUBLIC_COMMANDS = [
	'getmarketsummaries',
	'getcurrencies',
	'getwallethealth',
	'getmarketsummary',
	'getmarketorderbook',
	'getmarkets',
	'GetTicks',
	]

PRIVATE_COMMANDS = [
	'getopenorders',
	'getorder',
	'getorderhistory',
	'tradecancel',
	'getbalance',
	'getbalances',
	'withdraw',
	'tradebuy',
	'tradesell',
	'getwithdrawalhistory',
	'getpendingdeposits',
	'getdeposithistory',
	'getdepositaddress',
	'generatedepositaddress',	
	]


class BittrexError(Exception):
	"""
	Exception for catch invalid commands and other repsonses
	that don't match with 200 code responses.
	""" 
	def __init__(self, err):
		pass

class Bittrex(object):
	"""
	Used for requesting Bittrex with API key and API secret.

	"""
	def __init__(self, api_key=None, api_secret=None, 
				timeout=5, parse_float=Decimal, parse_int=int,
				debug_endpoint=False):
		"""
		Key and secret not needed for public commands.

		:param api_key: Api key supplied by Bittrex
		:type api_key: str
		
		:param api_secret: Api secret supplied by Bittrex
		:type api_secret: str
		
		:param timeout: time in sec to wait for an api response
			(otherwise 'requests.exceptions.TimeoutError' is raised)
			(default == 5)
		:type timeout: int
		
		:param parse_float: parser used by json.loads() for
			retrieve float type returns (default == Decimal)
		:type parse_float: any

		:param parse_float: parser used by json.loads() for
			retrieve int type returns (default == int)
		:type parse_float: any
		
		:param debug_endpoint: With True prints url endpoint
			used in calls (default == False)
		:type debug_endpoint: bool

		"""
		self.api_key = str(api_key) if api_key else None
		self.api_secret = str(api_secret) if api_secret else None
		self.timeout = timeout
		self.parse_float, self.parse_int = \
			parse_float, parse_int
		self.debug_endpoint = debug_endpoint

	@property
	def nonce(self):
		self._nonce = int(time()*1000)
		return self._nonce

	def __call__(self, group, command, args={}):
		"""
		Queries Bittrex with given method and args
		- encodes and sends <command> with optional [args] to Poloniex api
		- raises 'bittrex.BittrexError' if an api key or secret is missing
			(and the command is 'private') or if the <command> is not valid
		- returns decoded json api message
		
		:param group: Param for queries classification in API
		:type command: str

		:param command: Query method for getting info
		:type command: str

		:param args: Extra options for query
		:type args: dict

		:return: JSON response from Bittrex
		:rtype : dict
		"""

		from requests.exceptions import ReadTimeout, ConnectionError
		base_url = 'https://bittrex.com/Api/v2.0/'

		if command in PRIVATE_COMMANDS:
			if not self.api_key or not self.api_secret:
				raise BittrexError("Key and Secret needed!")
			url = base_url + 'key/{}/{}?'.format(group, command)

			args['nonce'] = self.nonce
			args['apikey'] = self.api_key
			url += _urlencode(args)

			if self.debug_endpoint == True:
				print(url)

			sign = _new(self.api_secret.encode('utf-8'),
						url.encode('utf-8'),_sha512).hexdigest()
			# post request
			ret = _get(url, headers={'apisign': sign},
						timeout=self.timeout)

			if ret.status_code != 200:
				raise BittrexError("Status Code: %s" % ret.status_code)

			jsonout = _loads(ret.text,
							 parse_float=self.parse_float,
							 parse_int=self.parse_int)
			return jsonout

		elif command in PUBLIC_COMMANDS:
			base_url += 'pub/{}/'.format(group)

			url = base_url + command + '?' + _urlencode(args)

			if self.debug_endpoint == True:
				print(url)

			ret = _get(url, timeout=self.timeout)

			if ret.status_code != 200:
				raise BittrexError("Status Code: %s" % ret.status_code)

			jsonout = _loads(ret.text,
							 parse_float=self.parse_float,
							 parse_int=self.parse_int)
			return jsonout
		else:
			raise BittrexError("Invalid Command: %s" % command)

	""" ###########################################
		############  PUBLIC COMMANDS  ############
		###########################################
	"""

	def get_markets(self):
		"""
		Used to get all markets available at Bittrex
		along with other meta data.

		pub/markets/getmarkets

		:return: Available market info in JSON
		:rtype : dict
		"""
		return self.__call__('markets', 'getmarkets')

	def get_market_summary(self, market):
		"""
		Used to get information about a given market 
		
		:param market: String literal for the market (ex: BTC-LTC)
		:type market: str

		pub/market/getmarketsummary?marketname=<market>

		:return: Available market summary in JSON
		:rtype : dict
		"""
		return self.__call__('market', 'getmarketsummary', 
							{'marketname': market})

	def get_market_summaries(self):
		"""
		Used to get the open and available trading markets
		at Bittrex along with other meta data.

		pub/markets/getmarketsummaries

		:return: Available markets summaries info in JSON
		:rtype : dict
		"""
		return self.__call__('markets', 'getmarketsummaries')

	def get_currencies(self):
		"""
		Used to get all availables currencies
		at Bittrex along with other meta data.
		
		pub/currencies/getcurrencies

		:return: Available currencies info in JSON
		:rtype : dict
		"""
		return self.__call__('currencies', 'getcurrencies')

	def get_wallet_health(self):
		"""
		Used to get information about all
		availables currencies status at Bittrex 
		along with other meta data.

		pub/currencies/getwallethealth

		:return: Available currencies status info in JSON
		:rtype : dict
		"""
		return self.__call__('currencies', 'getwallethealth')


	def get_market_orderbook(self, market):
		"""
		Used to get information about a given market orderbook
		
		pub/currencies/getmarketorderbook

		:param market: String literal for the market (ex: BTC-LTC)
		:type market: str

		:return: Market orderbook info in JSON
		:rtype : dict
		"""
		return self.__call__('market', 'getmarketorderbook',
							{'marketname': market})

	def get_ticks(self, market, period):
		"""
		Used to data chart information about a given market 
		in a given period.
		
		pub/market/GetTicks?marketName=<market>&tickInterval=<period>

		:param market: String literal for the market (ex: BTC-LTC)
		:type market: str

		:param period: Period between ticks (i.e hour)
			periods -> ["oneMin", "fiveMin", "thirtyMin", "hour", "day"]
		:type period: str

		:return: Market historical chart data info in JSON
		:rtype : dict
		"""
		return self.__call__('market', 'GetTicks',
							{'marketName': market,
							 'tickInterval': period})

	""" ###########################################
		###########  PRIVATE COMMANDS  ############
		###########################################
	"""
	def get_order(self, uuid):
		"""
		Returns information about a specific order (by UUID)
		
		:param uuid: String literal for the orderId
		:type uuid: str

		:return: Information of given order
		:rtype : dict
		"""
		return self.__call__('orders', 'getorder',
							{'orderid': uuid})

	def get_open_orders(self, market=None):
		""" 
		Returns all of your currently open orders if
		market == None, else returns all of your
		currently open orders in the given market.
		
		:param market: String literal for the market (optional)
		:type market: str

		:return: Currently open orders
		:rtype : dict
		"""
		if market:
			return self.__call__('market', 'getopenorders',
								 {'marketname': market})
		return self.__call__('orders', 'getopenorders')

	def get_order_history(self):
		""" 
		Returns all of your order history

		:return: Currently order history
		:rtype : dict
		"""
		return self.__call__('orders', 'getorderhistory')

	def get_balance(self, currency=None):
		"""
		Returns all of your currently balance if
		market == None, else returns your balance
		for a given currency.
		
		:param currency: String literal for the currency (optional)
		:type market: str

		:return: Currently balance
		:rtype : dict
		"""
		if currency:
			return self.__call__('balance', 'getbalance',
								 {'currencyname': currency})
		return self.__call__('balance', 'getbalances')

	def cancel(self, uuid):
		"""
		Cancel an order by given uuid
		
		:param uuid: String literal for the orderId
		:type uuid: str

		:return: Message of success/fail
		:rtype : dict

		Invalid uuid response:	{'message': 'INVALID_ORDER',  (str)
								 'success': False,			  (bool)
								 'result': None}			  (NoneType)

		Successed response: 	{'success': True,  
								 'result': None,
								 'message': ''}
		"""
		return self.__call__('market', 'tradecancel',
							 {'orderId': uuid})

	def withdraw(self, currency, amount, address):
		"""
		Withdraws a specific amount of a certain 
		currency to the specified address

		:param currency: Currency symbol to withdraw
		:type currency: str

		:param amount: Quantity to withdraw
		:type amount: str, float or int

		:param address: Address to send your withdrawal
		:type amount: str
		"""
		return self.__call__('balance', 'withdrawcurrency',
							 {"currencyname": currency, 
							  "quantity": amount, 
							  "address": address})

	def place_order(self, tradetype, market, amount, rate,
					ordertype, timeInEffect, 
					conditionType=None, target=None):
		"""	
		Places a buy/sell order with specific conditions 
		(target only required if a condition is in place)


		"""

		if tradetype in ('BUY', 'buy'):
			method = "tradebuy"
		elif tradetype in ('SELL', 'sell'):
			method = "tradesell"

		if not conditionType:
			conditionType = "CONDITION_NONE"
		if not target:
			target = "0"
		options = {"marketname": market, 
				   "ordertype": ordertype, 
				   "quantity": str(amount),
				   "rate": str(rate),
				   "timeineffect": str(timeInEffect),
				   "conditiontype": conditionType,
				   "target": target}

		return self.__call__('market', method, options)

	def get_withdrawal_history(self, currency=None):
		"""
		Returns your complete withdrawal history if
		currency == None, else returns your withdrawal
		history for a given currency 

		:param currency: String literal for the currency (optional)
		:type market: str

		:return: Currently withdrawal history
		:rtype : dict
		"""
		if not currency:
			currency = ""
		return self.__call__('balance', "getwithdrawalhistory", 
							 {"currencyname": currency})

	def get_deposit_history(self, currency=None):
		"""
		Returns your deposits history for all currencies 
		if currency == None, else returns your deposit history
		history for a given currency 

		:param currency: String literal for the currency (optional)
		:type market: str

		:return: Currently deposits history
		:rtype : dict
		"""
		if not currency:
			currency = ""
		return self.__call__('balance', "getdeposithistory", 
							 {"currencyname": currency})

	def get_pending_deposits(self, currency=None):
		"""
		Returns your pending deposits for all currencies 
		if currency == None, else returns your pending  
		deposits for a given currency 

		:param currency: String literal for the currency (optional)
		:type market: str

		:return: Currently pending deposits
		:rtype : dict
		"""
		if not currency:
			currency = ""
		return self.__call__('balance', "getpendingdeposits", 
							 {"currencyname": currency})

	def get_deposit_address(self, currency):
		"""
		Returns your deposit address for a specified currency 

		:param currency: String literal for the currency
		:type market: str

		:return: Deposit address
		:rtype : dict
		"""
		return self.__call__('balance', "getdepositaddress", 
							 {"currencyname": currency})

	def generate_deposit_address(self, currency):
		"""
		Generate a deposit address for a specified currency 

		:param currency: String literal for the currency
		:type market: str

		:return: Deposit address
		:rtype : dict
		"""
		return self.__call__('balance', "generatedepositaddress", 
							 {"currencyname": currency})








