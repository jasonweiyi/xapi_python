# -*- coding: utf-8 -*-
import os
from base.abstract_xapi import AbstractXApi
from base.comm import *

__author__ = 'Chunyou<snowtigersoft@126.com>'

os.environ['PATH'] = ';'.join([os.path.dirname(__file__) + "\\include",
                               os.path.dirname(__file__) + "\\include\\LTS\\win32",
                               os.environ['PATH']])


class XApi(AbstractXApi):
    p_lib = None
    p_fun = None
    p_api = None
    _x_response = None

    def __init__(self, lib_path, is_market=True):
        super(XApi, self).__init__("QuantBox_XAPI", lib_path, is_market)
        self._x_response = fnOnRespone(self._on_response)

    def init(self):
        """
        load the lib
        :return:
        """
        self.invoke_log('on_invoke_init')
        if self._xapi:
            func = self._xapi.X_LoadLib
            func.restype = c_void_p
            func.argtypes = [c_char_p]
            self.p_lib = func(self._lib_path)
            if self.p_lib:
                func = self._xapi.X_GetFunction
                func.restype = c_void_p
                func.argtypes = [c_void_p, c_char_p]
                self.p_fun = func(self.p_lib, b"XRequest")
                if self.p_fun:
                    return True
        return False

    def get_last_error(self):
        self.invoke_log('on_invoke_get_last_error')
        if self._xapi:
            func = self._xapi.X_GetLastError
            func.restype = c_char_p
            func.argtypes = []
            ptr = func()
            return ptr.decode('gbk')

    def get_api_type(self):
        self.invoke_log('on_invoke_get_api_type')
        if self._xapi:
            func = self._xapi.X_GetApiType
            func.restype = ApiType
            func.argtypes = [c_void_p]
            return func(self.p_fun)

    def get_api_version(self):
        self.invoke_log('on_invoke_get_api_version')
        if self._xapi:
            func = self._xapi.X_GetApiVersion
            func.restype = c_char_p
            func.argtypes = [c_void_p]
            ptr = func(self.p_fun)
            return ptr.value

    def get_api_name(self):
        self.invoke_log('on_invoke_get_api_name')
        if self._xapi:
            func = self._xapi.X_GetApiName
            func.restype = c_char_p
            func.argtypes = [c_void_p]
            ptr = func(self.p_fun)
            return ptr

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
        if self._xapi:
            func = self._xapi.X_Create
            func.restype = c_void_p
            func.argtypes = [c_void_p]
            self.p_api = func(self.p_fun)

            func = self._xapi.X_Register
            func.restype = None
            func.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
            func(self.p_fun, self.p_api, self._x_response, id(self))

            func = self._xapi.X_Connect
            func.restype = None
            func.argtypes = [c_void_p, c_void_p, c_char_p, POINTER(ServerInfoField), POINTER(UserInfoField), c_int]
            func(self.p_fun, self.p_api, path, byref(server_info), byref(user_info), count)

    def disconnect(self):
        self.invoke_log('on_invoke_disconnect')
        if self._xapi:
            func = self._xapi.X_Disconnect
            func.restype = None
            func.argtypes = [c_void_p, c_void_p]
            func(self.p_fun, self.p_api)

            func = self._xapi.X_FreeLib
            func.restype = None
            func.argtypes = [c_void_p]
            func(self.p_lib)

            self.p_lib = None
            self.p_fun = None
            self.p_api = None

    def subscribe(self, instrument_ids, exchange_id=b''):
        """
        Subscribe market data for the given instruments.
        :param instrument_ids: [string], list of instrument ids.
        :param exchange_id: string, exchange id
        """
        self.invoke_log('on_invoke_subscribe', instrument_ids=instrument_ids, exchange_id=exchange_id)
        if self._xapi:
            func = self._xapi.X_Subscribe
            func.restype = None
            func.argtypes = [c_void_p, c_void_p, c_char_p, c_char_p]
            func(self.p_fun, self.p_api, c_char_p(
                b','.join(instrument_ids) if isinstance(instrument_ids, list) else instrument_ids),
                c_char_p(exchange_id))

    def unsubscribe(self, instrument_ids, exchange_id=b''):
        """
         Un-subscribe market data for the given instruments.
        :param instrument_ids: [string], list of instrument ids.
        :param exchange_id: string, exchange id
        """
        self.invoke_log('on_invoke_unsubscribe', instrument_ids=instrument_ids, exchange_id=exchange_id)
        if self._xapi:
            func = self._xapi.X_Unsubscribe
            func.restype = None
            func.argtypes = [c_void_p, c_void_p, c_char_p, c_char_p]
            func(self.p_fun, self.p_api, c_char_p(
                b','.join(instrument_ids) if isinstance(instrument_ids, list) else instrument_ids),
                c_char_p(exchange_id))

    def subscribe_quote(self, instrument_ids, exchange_id=b''):
        """
        Subscribe market data for the given instruments.
        :param instrument_ids: [string], list of instrument ids.
        :param exchange_id: string, exchange id
        """
        self.invoke_log('on_invoke_subscribe_quote', instrument_ids=instrument_ids, exchange_id=exchange_id)
        if self._xapi:
            func = self._xapi.X_SubscribeQuote
            func.restype = None
            func.argtypes = [c_void_p, c_void_p, c_char_p, c_char_p]
            func(self.p_fun, self.p_api, c_char_p(
                b','.join(instrument_ids) if isinstance(instrument_ids, list) else instrument_ids),
                c_char_p(exchange_id))

    def unsubscribe_quote(self, instrument_ids, exchange_id=b''):
        """
         Un-subscribe market data for the given instruments.
        :param instrument_ids: [string], list of instrument ids.
        :param exchange_id: string, exchange id
        """
        self.invoke_log('on_invoke_unsubscribe_quote', instrument_ids=instrument_ids, exchange_id=exchange_id)
        if self._xapi:
            func = self._xapi.X_UnsubscribeQuote
            func.restype = None
            func.argtypes = [c_void_p, c_void_p, c_char_p, c_char_p]
            func(self.p_fun, self.p_api, c_char_p(
                b','.join(instrument_ids) if isinstance(instrument_ids, list) else instrument_ids),
                c_char_p(exchange_id))

    def req_qry_instrument(self, instrument_id, exchange_id):
        """
        get instrument info
        :param instrument_id: string
        :param exchange_id: string, exchange id
        :return:
        """
        self.invoke_log('on_invoke_req_qry_instrument', instrument_id=instrument_id, exchange_id=exchange_id)
        if self._xapi:
            func = self._xapi.X_ReqQryInstrument
            func.restype = None
            func.argtypes = [c_void_p, c_void_p, c_char_p, c_char_p]
            func(self.p_fun, self.p_api, c_char_p(instrument_id), c_char_p(exchange_id))

    def req_qry_investor_position(self, instrument_id, exchange_id):
        """
        get investor position
        :param instrument_id: string
        :param exchange_id: string
        :return:
        """
        self.invoke_log('on_invoke_req_qry_investor_position', instrument_id=instrument_id, exchange_id=exchange_id)
        if self._xapi:
            func = self._xapi.X_ReqQryInvestorPosition
            func.restype = None
            func.argtypes = [c_void_p, c_void_p, c_char_p, c_char_p]
            func(self.p_fun, self.p_api, c_char_p(instrument_id), c_char_p(exchange_id))

    def req_qry_trading_account(self):
        """
        get trading account info
        :return:
        """
        self.invoke_log('on_invoke_req_qry_trading_account')
        if self._xapi:
            func = self._xapi.X_ReqQryTradingAccount
            func.restype = None
            func.argtypes = [c_void_p, c_void_p]
            func(self.p_fun, self.p_api)

    def send_order(self, order, in_out, count):
        """
        create a new order
        :param order:
        :param in_out:
        :param count:
        :return:
        """
        self.invoke_log('on_invoke_send_order', order=order, in_out=in_out, count=count)
        if self._xapi:
            func = self._xapi.X_SendOrder
            func.restype = None
            func.argtypes = [c_void_p, c_void_p, POINTER(OrderField), POINTER(OrderIDType), c_int]
            func(self.p_fun, self.p_api, byref(order), byref(in_out), count)

    def cancel_order(self, p_in, p_out, count):
        """
        cancel an order
        :param p_in:
        :param p_out:
        :param count:
        :return:
        """
        self.invoke_log('on_invoke_cancel_order', p_in=p_in, p_out=p_out, count=count)
        if self._xapi:
            func = self._xapi.X_CancelOrder
            func.restype = None
            func.argtypes = [c_void_p, c_void_p, POINTER(OrderIDType), POINTER(OrderIDType), c_int]
            func(self.p_fun, self.p_api, byref(p_in), byref(p_out), count)

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
        if self._xapi:
            func = self._xapi.X_SendQuote
            func.restype = None
            func.argtypes = [c_void_p, c_void_p, POINTER(QuoteField), POINTER(OrderIDType), POINTER(OrderIDType), c_int]
            func(self.p_fun, self.p_api, byref(quote), byref(ask_out), byref(bid_out), count)

    def cancel_quote(self, p_in, p_out, count):
        """
        cancel a quote
        :param p_in:
        :param p_out:
        :param count:
        :return:
        """
        self.invoke_log('on_invoke_cancel_quote', p_in=p_in, p_out=p_out, count=count)
        if self._xapi:
            func = self._xapi.X_CancelQuote
            func.restype = None
            func.argtypes = [c_void_p, c_void_p, POINTER(OrderIDType), POINTER(OrderIDType), c_int]
            func(self.p_fun, self.p_api, byref(p_in), byref(p_out), count)
