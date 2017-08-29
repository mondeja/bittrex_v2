#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
	from urllib import urlencode as _urlencode
	str = unicode
# python 3
except:
	from urllib.parse import urlencode as _urlencode

from json import loads as _loads
from hmac import new as _new
from hashlib import sha512 as _sha512
from time import time, sleep
import logging
# 3rd party
#from requests.exceptions import RequestException
from requests import post as _post
from requests import get as _get
from decimal import Decimal

PUBLIC_METHODS = [
	'getmarketsummaries',
	'',
	]

class BittrexError(Exception):
	def __init__(self, err):
		print(err)

class Bittrex(object):
	"""
	Used for requesting Bittrex with API key and API secret

	"""
	def __init__(self, api_key, api_secret, timeout=1,
				parse_float=Decimal, parse_int=int):
		"""
		api_key = str api key supplied by Bittrex
		api_secret = str secret hash supplied by Poloniex
		timeout = int time in sec to wait for an api response
			(otherwise 'requests.exceptions.TimeoutError' is raised)
		# Time Placeholders # (MONTH == 30*DAYS)
		self.MINUTE, self.HOUR, self.DAY, self.WEEK, self.MONTH, self.YEAR
		"""
		self.api_key = str(api_key) if api_key else None
		self.api_secret = str(api_secret) if api_secret else None
		self.logger = logger
		self.timeout = timeout
		self.parse_float, self.parse_int = \
			parse_float, parse_int

	@property
	def nonce(self):
		self._nonce = int(time()*1000)
		return self._nonce

	def __call__(self, command, args={}):
		"""
		Queries Bittrex with given method and args
		- encodes and sends <command> with optional [args] to Poloniex api
		- raises 'bittrex.BittrexError' if an api key or secret is missing
			(and the command is 'private') or if the <command> is not valid
		- returns decoded json api message
		
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
				raise BittrexError("A Key and Secret needed!")
			pass
		elif command in PUBLIC_COMMANDS:
			ret = _get('https://poloniex.com/public?' + _urlencode(args),
						timeout=self.timeout)
			
			jsonout = _loads(ret.text,
							 parse_float=Decimal,
							 parse_int=int)
			return jsonout

	def get_market_summaries(self):
		"""
		Used to get the open and available trading markets
		at Bittrex along with other meta data.

		:return: Available market info in JSON
		:rtype : dict
		"""
		return self.__call__('getmarketsummaries')
