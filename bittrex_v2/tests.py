#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from bittrex import Bittrex, BittrexError
from decimal import Decimal
from datetime import datetime


""" ###########################################
	#########  TESTS CONFIGURATION  ###########
	###########################################
"""

class ConfigTest:
	"""
	Configuration for Bittrex API V2 tests. 
	
	:param ORDER_UUID: Closed order UUID for test get_order() method
	:type ORDER_UUID: str

	:param SHOW_ENDPOINTS: Show url endpoints in 
		tests (True) or not (False)
	:type SHOW_ENDPOINTS: bool
	"""
	PAIR = 'BTC-ETH'
	COIN = 'BTC'

	SHOW_ENDPOINTS = True
	ORDER_UUID = ''

	def __init__(self):
		pass

config = ConfigTest()

""" ###########################################
	############  BITTREX TESTS  ##############
	###########################################
"""

def test_result(self, ret, result_type=list):
	self.assertEqual(ret['success'], True)
	self.assertEqual(ret['message'], "")
	if type(result_type) is list:
		self.assertIn(type(ret['result']), result_type)
	else:
		self.assertIs(type(ret['result']), result_type)

class TestPublicBittrex(unittest.TestCase):
	"""
	Integration tests for the Bittrex public commands. These will fail 
	in the absence of an internet connection or if Poloniex API goes down.
	"""
	def setUp(self):
		self.bittrex = Bittrex(timeout=10,
							   debug_endpoint=config.SHOW_ENDPOINTS,
							   parse_float=Decimal)

	def test_invalid_command(self):
		with self.assertRaises(BittrexError):
			self.bittrex.__call__('invalidgroup', 'invalidcommand')

	def test_get_markets(self):
		actual = self.bittrex.get_markets()
		test_result(self, actual)

		value_types = {"MarketCurrency": str, 
					   "BaseCurrency": str,
					   "MarketCurrencyLong": str, 
					   "BaseCurrencyLong": str,
					   "MinTradeSize": Decimal,
					   "MarketName": str,
					   "IsActive": bool,
					   "Created": str}
		multiple_value_types = (type(None), bool, str)

		for market in actual['result']:
			for key, value in market.items():
				if key in ("Notice", "IsSponsored", "LogoUrl"):
					self.assertIn(type(value), multiple_value_types)
				else:
					self.assertIs(type(value), value_types[key])

	def test_get_market_summary(self):
		actual = self.bittrex.get_market_summary(config.PAIR)
		test_result(self, actual, result_type=dict)
		
		value_types = {'High': Decimal, 
					   'Ask': Decimal, 
					   'Bid': Decimal, 
					   'TimeStamp': str, 
					   'BaseVolume': Decimal,
					   'OpenBuyOrders': int, 
					   'MarketName': str, 
					   'Created': str, 
					   'Volume': Decimal,
					   'PrevDay': Decimal, 
					   'Low': Decimal, 
					   'OpenSellOrders': int, 
					   'Last': Decimal}

		for key, value in actual['result'].items():
			self.assertIs(type(value), value_types[key])

	def test_get_market_summaries(self):
		actual = self.bittrex.get_market_summaries()
		test_result(self, actual)

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
		test_result(self, actual)

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
		test_result(self, actual)

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

	def test_get_market_orderbook(self):
		actual = self.bittrex.get_market_orderbook(config.PAIR)
		test_result(self, actual, result_type=dict)

		books, keys = (('buy', 'sell'), ('Quantity', 'Rate'))
		for b in books:
			self.assertIs(type(actual['result'][b]), list)
			
			for order in actual['result'][b]:
				for k in keys:
					self.assertIs(type(order[k]), Decimal)

	def test_get_ticks(self):
		valid_periods = ("oneMin", "fiveMin", 
						 "thirtyMin", "hour", "day")

		for period in valid_periods:
			actual = self.bittrex.get_ticks(config.PAIR, period)
			test_result(self, actual)
			
			for tick in actual['result']:
				for key, value in tick.items():
					if key == 'T':
						self.assertIs(type(value), str)
					else:
						self.assertIs(type(value), Decimal)


class TestPrivateBittrex(unittest.TestCase):
	"""
	Integration tests for the Bittrex account commands. These will fail 
	in the absence of an internet connection, if Bittrex API goes down
	or if secrets.json file is not correctly configured.
	"""

	def setUp(self):
		import json
		with open('secrets.json') as secrets_file:
			secrets = json.load(secrets_file)

		self.bittrex = Bittrex(api_key=secrets['key'],
							   api_secret=secrets['secret'],
							   timeout=10, 
							   debug_endpoint=config.SHOW_ENDPOINTS,
							   parse_float=Decimal)

	def test_get_open_orders(self):
		actual = self.bittrex.get_open_orders()
		test_result(self, actual)
		

		value_types = {'ImmediateOrCancel': bool,
					   'Limit': Decimal, 
					   'CancelInitiated': bool, 
					   'Opened': str, 
					   'Exchange': str, 
					   'Updated': str, 
					   'Price': Decimal, 
					   'QuantityRemaining': Decimal,
					   'Closed': [type(None), str], 
					   'OrderUuid': str, 
					   'OrderType': str, 
					   'IsOpen': bool, 
					   'Uuid': str, 
					   'CommissionPaid': Decimal, 
					   'Quantity': Decimal, 
					   'IsConditional': bool, 
					   'Id': int, 
					   'Condition': str, 
					   'ConditionTarget': [type(None), str], 
					   'PricePerUnit': [type(None), Decimal]
					   }

		orders = actual['result']
		if len(orders) > 0:
			for o in orders:
				for key, value in o.items():
					if type(value_types[key]) is list:
						self.assertIn(type(value), value_types[key])
					else:
						self.assertIs(type(value), value_types[key])

	def test_get_order(self):
		uuid = config.ORDER_UUID
		start_test = uuid != '' and type(uuid) is str

		if start_test == True:
			actual = self.bittrex.get_order(uuid)
			test_result(self, actual, result_type=[type(None), dict])
			if type(actual) is type(None):
				print('Order {} not found'.format(uuid))
				print('Provide a closed order uuid on ConfigTest().ORDER_UUID')
				print('Test for method get_order() incompleted.')
			elif type(actual) is dict:
				value_types = {'Limit': Decimal, 
							   'Exchange': str, 
							   'CommissionReserved': Decimal, 
							   'QuantityRemaining': Decimal, 
							   'IsConditional': bool, 
							   'OrderUuid': str, 
							   'CancelInitiated': bool, 
							   'Closed': str, 
							   'Quantity': Decimal, 
							   'Sentinel': str, 
							   'Reserved': Decimal, 
							   'CommissionPaid': Decimal, 
							   'PricePerUnit': Decimal, 
							   'ConditionTarget': [type(None), str], 
							   'ReserveRemaining': Decimal, 
							   'ImmediateOrCancel': bool, 
							   'Opened': str, 
							   'AccountId': [type(None), str], 
							   'IsOpen': bool, 
							   'Condition': str, 
							   'CommissionReserveRemaining': Decimal, 
							   'Price': Decimal, 
							   'Type': str}
				for key, value in actual['result'].items():
					if type(value_types[key]) is list:
						self.assertIn(type(value), value_types[key])
					else:
						self.assertIs(type(value), value_types[key])

			else:
				msg = "type(actual['result']) is {}".format(type(actual['result']))
				raise AssertionError(msg)

	def test_get_order_history(self):
		actual = self.bittrex.get_order_history()
		test_result(self, actual)

		value_types = {'Quantity': Decimal, 
					   'Condition': str, 
					   'ImmediateOrCancel': bool, 
					   'Limit': Decimal, 
					   'PricePerUnit': Decimal,
					   'OrderUuid': str,
					   'IsConditional': bool, 
					   'TimeStamp': str, 
					   'Exchange': str, 
					   'OrderType': str, 
					   'QuantityRemaining': Decimal, 
					   'Commission': Decimal, 
					   'Price': Decimal, 
					   'ConditionTarget': [type(None), str], 
					   'Closed': str}
		if len(actual['result']) > 0:
			for o in actual['result']:
				self.assertIs(type(o), dict)
				for key, value in o.items():
					if type(value_types[key]) is list:
						self.assertIn(type(value), value_types[key])
					else:
						self.assertIs(type(value), value_types[key])

	def test_get_balance(self):
		""" Test for all currencies balances """
		actual = self.bittrex.get_balance()
		test_result(self, actual)

		markets_names = ('EthereumMarket', 
						 'FiatMarket',
						 'BitcoinMarket')

		markets_value_types = {'BaseVolume': Decimal,
							   'High': Decimal,
							   'Created': str, 
							   'Last': Decimal, 
							   'Bid': Decimal, 
							   'TimeStamp': str, 
							   'Ask': Decimal, 
							   'OpenSellOrders': int, 
							   'Low': Decimal, 
							   'OpenBuyOrders': int, 
							   'Volume': Decimal, 
							   'PrevDay': Decimal, 
							   'MarketName': str}

		balance_value_types = {'Updated': [type(None), str], 
							   'Requested': [type(None), bool],  
							   'Pending': Decimal, 
							   'AutoSell': [type(None), bool], 
							   'Available': Decimal, 
							   'AccountId': [type(None), int],  
							   'CryptoAddress': [type(None), str], 
							   'Uuid': [type(None), str], 
							   'Balance': Decimal, 
							   'Currency': str}

		currency_value_types = {'CurrencyLong': str,
								'CoinType': str, 
								'TxFee': Decimal, 
								'IsActive': bool, 
								'MinConfirmation': int, 
								'Notice': [type(None), str, Decimal], 
								'BaseAddress': [type(None), str], 
								'Currency': str}

		for c in actual['result']:
			self.assertIs(type(c), dict)
			for _key, _value in c.items():
				if _key in markets_names:
					self.assertIn(type(_value), (type(None), dict))
					if _value:
						for key, value in _value.items():
							self.assertIs(type(value), markets_value_types[key])
				elif _key == 'Balance':
					self.assertIs(type(_value), dict)
					for key, value in _value.items():
						if type(balance_value_types[key]) is list:
							self.assertIn(type(value), balance_value_types[key])
						else:
							self.assertIs(type(value), balance_value_types[key])
				elif _key == 'Currency':
					self.assertIs(type(_value), dict)
					for key, value in _value.items():
						if type(currency_value_types[key]) is list:
							self.assertIn(type(value), currency_value_types[key])
						else:
							self.assertIs(type(value), currency_value_types[key])
				else:
					raise AssertionError('Change in API V2! -> get_balances()')


		""" Test for one currency balance """
		actual = self.bittrex.get_balance(config.COIN)
		test_result(self, actual, result_type=dict)

		for key, value in actual['result'].items():
			if type(balance_value_types[key]) is list:
				self.assertIn(type(value), balance_value_types[key])
			else:
				self.assertIs(type(value), balance_value_types[key])

	def test_get_withdrawal_history(self):
		def test(call):
			test_result(self, call)
		
			value_types = {'PaymentUuid': str,
						   'Amount': Decimal, 
						   'Opened': str, 
						   'Authorized': bool, 
						   'Address': str, 
						   'Canceled': bool, 
						   'InvalidAddress': bool, 
						   'TxId': [str, type(None)], 
						   'TxCost': Decimal, 
						   'Currency': str, 
						   'PendingPayment': bool}

			if len(call['result']) > 0:
				for w in call['result']:
					self.assertIs(type(w), dict)
					for key, value in w.items():
						if type(value_types[key]) is list:
							self.assertIn(type(value), value_types[key])
						else:
							self.assertIs(type(value), value_types[key])

		test(self.bittrex.get_withdrawal_history())
		test(self.bittrex.get_withdrawal_history(config.COIN))

	def test_get_deposit_history(self):
		def test(call):
			test_result(self, call)

			value_types = {'TxId': [str, type(None)], 
						   'CryptoAddress': str, 
						   'Currency': str, 
						   'Confirmations': int, 
						   'Id': int, 
						   'Amount': Decimal, 
						   'LastUpdated': str}

			if len(call['result']) > 0:
				for w in call['result']:
					self.assertIs(type(w), dict)
					for key, value in w.items():
						if type(value_types[key]) is list:
							self.assertIn(type(value), value_types[key])
						else:
							self.assertIs(type(value), value_types[key])

		test(self.bittrex.get_deposit_history())
		test(self.bittrex.get_deposit_history(config.COIN))

	def test_get_pending_deposits(self):
		actual = self.bittrex.get_pending_deposits()
		test_result(self, actual)

	def test_get_deposit_address(self):
		actual = self.bittrex.get_deposit_address(config.COIN)
		test_result(self, actual, result_type=dict)

		for key, value in actual['result'].items():
			self.assertIs(type(value), str)

	def test_generate_deposit_address(self):
		actual = self.bittrex.generate_deposit_address(config.COIN)
		self.assertEqual(actual['message'], 'ADDRESS_GENERATING')

if __name__ == '__main__':
	unittest.main()