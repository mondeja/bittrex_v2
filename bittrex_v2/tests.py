#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from bittrex import Bittrex
from decimal import Decimal
from datetime import datetime


""" ###########################################
	#########  TESTS CONFIGURATION  ###########
	###########################################
"""

class ConfigTest:
	"""
	Configuration for Bittrex API tests. 
	"""
	PAIR = 'BTC-ETH'
	COIN = 'BTC'
	def __init__(self):
		pass

config = ConfigTest()

""" ###########################################
	############  BITTREX TESTS  ##############
	###########################################
"""

class TestPublicBittrex(unittest.TestCase):
	"""
	Integration tests for the Bittrex public commands. These will fail 
	in the absence of an internet connection or if Poloniex API goes down.
	"""
	def setUp(self):
		self.bittrex = Bittrex(timeout=5)

	def test_result(self, ret):
		self.assertEqual(ret['success'], True)
		self.assertEqual(ret['message'], "")
		self.assertIs(type(ret['result']), list)

	def test_get_market_summaries(self):
		actual = self.bittrex.get_market_summaries()
		self.test_result(actual)

		self.assertEqual(len(actual['result']) > 0, True)
		self.assertIs(type(actual['result'][0]), dict)

		for market in actual['result']:
			value_types = {"MarketCurrency": str, 
						   "BaseCurrency": str,
						   "MarketCurrencyLong": str,
						   "BaseCurrencyLong": str,
						   "MinTradeSize": Decimal,
						   "MarketName": str,
						   "IsActive": bool,
						   "Created": str}
			multiple_value_types = (type(None), bool, str)

			self.assertIs(type(market['Market']), dict)
			for key, value in market['Market'].items():
				if key in ("Notice", "IsSponsored", "LogoUrl"):
					self.assertIn(type(value), multiple_value_types)
				else:
					self.assertIs(type(value), value_types[key])

			self.assertIs(type(market['Summary']), dict)
			decimal_keys = ("High", "Low", "Volume", "Last",
							"BaseVolume", "Bid", "Ask", "PrevDay")
			int_keys = ("OpenBuyOrders", "OpenSellOrders")
			str_keys = ("TimeStamp", "Created", "MarketName")
			for key, value in market['Summary'].items():
				if key in decimal_keys:
					self.assertIs(type(value), Decimal)
				elif key in int_keys:
					self.assertIs(type(value), int)
				elif key in str_keys:
					self.assertIs(type(value), str)
				else:
					raise AssertionError(key, value)

			self.assertIs(type(actual['result'][0]['IsVerified']), bool)

	def test_get_currencies(self):
		actual = self.bittrex.get_currencies()
		self.test_result(actual)

		self.assertEqual(len(actual['result']) > 0, True)
		self.assertIs(type(actual['result'][0]), dict)

		for currency in actual['result']:
			value_types = {'CoinType': str, 
							'TxFee': Decimal, 
							'MinConfirmation': int, 
							'IsActive': bool, 
							'CurrencyLong': str, 
							'Currency': str}
			multiple_value_types = (type(None), bool, str)

			for key, value in currency.items():
				if key in ('Notice', 'BaseAddress'):
					self.assertIn(type(value), multiple_value_types)
				else:
					self.assertIs(type(value), value_types[key])

	def test_get_wallet_health(self):
		actual = self.bittrex.get_wallet_health()
		self.test_result(actual)

		self.assertEqual(len(actual['result']) > 0, True)
		self.assertIs(type(actual['result'][0]), dict)

		for currency in actual['result']:
			value_types = {"Currency": str, 
						   "DepositQueueDepth": int,
						   "WithdrawQueueDepth": int, 
						   "BlockHeight": int,
						   "WalletBalance": Decimal, 
						   "WalletConnections": int,
						   "MinutesSinceBHUpdated": int, 
						   "LastChecked": str,
						   "IsActive": bool}
			for key, value in currency['Health'].items():
				self.assertIs(type(value), value_types[key])

			value_types = {"Currency": str, "CurrencyLong": str,
						   "MinConfirmation": int, "TxFee": Decimal,
						   "IsActive": bool, "CoinType": str}
			multiple_value_types = (type(None), bool, str)
			for key, value in currency['Currency'].items():
				if key in ("BaseAddress", "Notice"):
					self.assertIn(type(value), multiple_value_types)
				else:
					self.assertIs(type(value), value_types[key])




class TestAccountBittrex(unittest.TestCase):
	"""
	Integration tests for the Bittrex account commands. These will fail 
	in the absence of an internet connection, if Poloniex API goes down
	or if secrets/bittrex.json file is not correctly configured.
	"""

	def setUp(self):
		import json
		with open('secrets/bittrex.json') as secrets_file:
			secrets = json.load(secrets_file)
		self.bittrex = Exchange('bittrex', 
								keys={'KEY': secrets['key'],
									  'SECRET': secrets['secret']},
								market_delimiter=config.DELIMITER)

	def test_balance(self):
		actual = self.bittrex.balance(coin=coin)
		self.assertIs(type(actual), Decimal)

		actual = self.bittrex.balance()
		self.assertIs(type(actual), dict)
		for key, value in actual.items():
			self.assertIs(type(value), Decimal)

	def test_complete_balance(self):
		actual = self.bittrex.complete_balance(coin=coin)
		self.assertIs(type(actual), dict)
		for key, value in actual.items():
			self.assertIs(type(value), Decimal)
		
		actual = self.bittrex.complete_balance()
		self.assertIs(type(actual), dict)
		for c, data in actual.items():
			self.assertIs(type(data), dict)
			for key, value in data.items():
				self.assertIs(type(value), Decimal)

	def test_open_orders(self):
		actual = self.bittrex.open_orders(pair=config.PAIR)
		self.assertIs(type(actual), list)
		value_types = {'amount': Decimal, 'total': Decimal,
						'price': Decimal, 'date': datetime,
						'orderId': str, 'type': str}
		if len(actual) > 0:
			for key, value in actual[0].items():
				self.assertIs(type(value), value_types[key])

		actual = self.bittrex.open_orders()
		print(actual)
		self.assertIs(type(actual), dict)
		for coin, orders in actual.items():
			self.assertIs(type(orders), list)
			if len(orders) > 0:
				for key, value in orders[0].items():
					self.assertIs(type(value), value_types[key])

	def test_deposit_address(self):
		actual = self.bittrex.deposit_address(coin=coin)
		self.assertIs(type(actual), str)
		
		if config.COMPLETE_TESTS == True:
			actual = self.bittrex.deposit_address()
			for coin, address in actual.items():
				self.assertIs(type(address), str)



if __name__ == '__main__':
	unittest.main()