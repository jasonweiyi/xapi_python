# -*- coding: utf-8 -*-
import os
from base.abstract_xapi import AbstractXApi
from base.comm import *

__author__ = 'Chunyou<snowtigersoft@126.com>'

os.environ['PATH'] = ';'.join([os.path.dirname(__file__) + "\\include",
                               os.path.dirname(__file__) + "\\include\\LTS\\win32",
                               os.environ['PATH']])


class XApiBacktesting(AbstractXApi):
    def __init__(self, lib_path, is_market=True):
        super(XApiBacktesting, self).__init__("QuantBox_XAPI", lib_path, is_market)

    def init(self):
        """
        load the lib
        :return:
        """
        self.invoke_log('on_invoke_init')
        return True

    def get_last_error(self):
        self.invoke_log('on_invoke_get_last_error')

    def get_api_type(self):
        self.invoke_log('on_invoke_get_api_type')
        return MarketData

    def get_api_version(self):
        self.invoke_log('on_invoke_get_api_version')
        return "0.1.0"

    def get_api_name(self):
        self.invoke_log('on_invoke_get_api_name')
        return "XApi Backtesing"

    def connect(self, path, server_info, user_info, count=0):
        """
        Connect to the server.
        :param path:
        :param server_info:
        :param user_info:
        :param count:
        :return:
        """
        self.invoke_log('on_invoke_connect', path=path, server_info=server_info, user_info=user_info, count=count)
        user_login_field = RspUserLoginField()
        user_login_field.TradingDay = '20150120'
        user_login_field.SessionID = '565656565'
        user_login_field.LoginTime = '07:22:07'
        self.make_response(OnConnectionStatus, p_api2=self, double1=ord(Logined.value), ptr1=user_login_field)
        self.make_response(OnConnectionStatus, p_api2=self, double1=ord(Done.value))

    def disconnect(self):
        self.invoke_log('on_invoke_disconnect')

    def subscribe(self, instrument_ids, exchange_id=b''):
        """
        Subscribe market data for the given instruments.
        :param instrument_ids: [string], list of instrument ids.
        :param exchange_id: string, exchange id
        """
        self.invoke_log('on_invoke_subscribe', instrument_ids=instrument_ids, exchange_id=exchange_id)

    def unsubscribe(self, instrument_ids, exchange_id=b''):
        """
         Un-subscribe market data for the given instruments.
        :param instrument_ids: [string], list of instrument ids.
        :param exchange_id: string, exchange id
        """
        self.invoke_log('on_invoke_unsubscribe', instrument_ids=instrument_ids, exchange_id=exchange_id)

    def subscribe_quote(self, instrument_ids, exchange_id=b''):
        """
        Subscribe market data for the given instruments.
        :param instrument_ids: [string], list of instrument ids.
        :param exchange_id: string, exchange id
        """
        self.invoke_log('on_invoke_subscribe_quote', instrument_ids=instrument_ids, exchange_id=exchange_id)

    def unsubscribe_quote(self, instrument_ids, exchange_id=b''):
        """
         Un-subscribe market data for the given instruments.
        :param instrument_ids: [string], list of instrument ids.
        :param exchange_id: string, exchange id
        """
        self.invoke_log('on_invoke_unsubscribe_quote', instrument_ids=instrument_ids, exchange_id=exchange_id)

    def req_qry_instrument(self, instrument_id, exchange_id):
        """
        get instrument info
        :param instrument_id: string
        :param exchange_id: string, exchange id
        :return:
        """
        self.invoke_log('on_invoke_req_qry_instrument', instrument_id=instrument_id, exchange_id=exchange_id)

    def req_qry_investor_position(self, instrument_id, exchange_id):
        """
        get investor position
        :param instrument_id: string
        :param exchange_id: string
        :return:
        """
        self.invoke_log('on_invoke_req_qry_investor_position', instrument_id=instrument_id, exchange_id=exchange_id)

    def req_qry_trading_account(self):
        """
        get trading account info
        :return:
        """
        self.invoke_log('on_invoke_req_qry_trading_account')

    def send_order(self, order, in_out, count):
        """
        create a new order
        :param order:
        :param in_out:
        :param count:
        :return:
        """
        self.invoke_log('on_invoke_send_order', order=order, in_out=in_out, count=count)

    def cancel_order(self, p_in, p_out, count):
        """
        cancel an order
        :param p_in:
        :param p_out:
        :param count:
        :return:
        """
        self.invoke_log('on_invoke_cancel_order', p_in=p_in, p_out=p_out, count=count)

    def send_quote(self, quote, ask_out, bid_out, count):
        """
        create a new quote
        :param quote:
        :param ask_out:
        :param bid_out:
        :param count:
        :return:
        """
        self.invoke_log('on_invoke_send_quote', quote=quote, ask_out=ask_out, bid_out=bid_out, count=count)

    def cancel_quote(self, p_in, p_out, count):
        """
        cancel a quote
        :param p_in:
        :param p_out:
        :param count:
        :return:
        """
        self.invoke_log('on_invoke_cancel_quote', p_in=p_in, p_out=p_out, count=count)
