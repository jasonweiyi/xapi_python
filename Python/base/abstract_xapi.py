# -*- coding: utf-8 -*-
__author__ = 'Chunyou<snowtigersoft@126.com>'

from .comm import *


class AbstractXApi(object):
    is_connected = False
    user_login_field = None
    _lib_path = None
    _callbacks = []
    _is_market = True
    _xapi = None
    debug = False

    def __init__(self, xapi_lib_path, lib_path, is_market=True):
        """
        create api from the lib_path
        :param lib_path:
        :return:
        """
        self._lib_path = lib_path
        self._is_market = is_market
        if xapi_lib_path:
            self._xapi = CDLL(xapi_lib_path)

    def init(self):
        """
        load the lib
        :return:
        """
        pass

    def get_last_error(self):
        pass

    def get_api_type(self):
        return Nono

    def get_api_version(self):
        return "0.1"

    def get_api_name(self):
        return 'AbstractXApi'

    def set_callbacks(self, callbacks):
        if not isinstance(callbacks, list):
            callbacks = [callbacks]
        self._callbacks = callbacks

    def connect(self, path, server_info, user_info, count):
        """
        Connect to the server.
        :param path:
        :param server_info:
        :param user_info:
        :param count:
        :return:
        """
        pass

    def disconnect(self):
        pass

    def subscribe(self, instrument_ids, exchange_id=b''):
        """
        Subscribe market data for the given instruments.
        :param instrument_ids: [string], list of instrument ids.
        :param exchange_id: string, exchange id
        """
        pass

    def unsubscribe(self, instrument_ids, exchange_id=b''):
        """
         Un-subscribe market data for the given instruments.
        :param instrument_ids: [string], list of instrument ids.
        :param exchange_id: string, exchange id
        """
        pass

    def subscribe_quote(self, instrument_ids, exchange_id=b''):
        """
        Subscribe market data for the given instruments.
        :param instrument_ids: [string], list of instrument ids.
        :param exchange_id: string, exchange id
        """
        pass

    def unsubscribe_quote(self, instrument_ids, exchange_id=b''):
        """
         Un-subscribe market data for the given instruments.
        :param instrument_ids: [string], list of instrument ids.
        :param exchange_id: string, exchange id
        """
        pass

    def req_qry_instrument(self, instrument_id, exchange_id):
        """
        get instrument info
        :param instrument_id: string
        :param exchange_id: string, exchange id
        :return:
        """
        pass

    def req_qry_investor_position(self, instrument_id, exchange_id):
        """
        get investor position
        :param instrument_id: string
        :param exchange_id: string
        :return:
        """
        pass

    def req_qry_trading_account(self):
        """
        get trading account info
        :return:
        """
        pass

    def send_order(self, p_order, p_in_out, count):
        """
        create a new order
        :param p_order:
        :param p_in_out:
        :param count:
        :return:
        """
        pass

    def cancel_order(self, p_in, p_out, count):
        """
        cancel an order
        :param p_in:
        :param p_out:
        :param count:
        :return:
        """
        pass

    def send_quote(self, p_quote, p_ask_out, p_bid_out, count):
        """
        create a new quote
        :param p_quote:
        :param p_ask_out:
        :param p_bid_out:
        :param count:
        :return:
        """
        pass

    def cancel_quote(self, p_in, p_out, count):
        """
        cancel a quote
        :param p_in:
        :param p_out:
        :param count:
        :return:
        """
        pass

    def _on_response(self, response_type, p_api1, p_api2, double1, double2, ptr1, size1, ptr2, size2, ptr3, size3):
        """
        callback from the queue
        :param response_type:
        :param p_api1:
        :param p_api2:
        :param double1:
        :param double2:
        :param ptr1:
        :param size1:
        :param ptr2:
        :param size2:
        :param ptr3:
        :param size3:
        :return:
        """
        if self.debug:
            print "Response: ", ord(response_type)
        if response_type == OnConnectionStatus.value:
            self._on_connect_status(p_api2, chr(int(double1)), ptr1, size1)
        elif self._callbacks:
            for callback in self._callbacks:
                if response_type == OnRtnDepthMarketData.value:
                    if self._is_market:
                        callback.on_market_rtn_depth_market_data_n(p_api2, ptr1)
                elif response_type == OnRspQryInstrument.value:
                    obj = cast(ptr1, POINTER(InstrumentField)).contents
                    callback.on_trading_rsp_qry_instrument(p_api2, obj, bool(double1))
                elif response_type == OnRspQryTradingAccount.value:
                    obj = cast(ptr1, POINTER(AccountField)).contents
                    callback.on_trading_rsp_qry_trading_account(p_api2, obj, bool(double1))
                elif response_type == OnRspQryInvestorPosition.value:
                    obj = cast(ptr1, POINTER(PositionField)).contents
                    callback.on_trading_rsp_qry_investor_position(p_api2, obj, bool(double1))
                elif response_type == OnRspQrySettlementInfo.value:
                    obj = cast(ptr1, POINTER(SettlementInfoField)).contents
                    callback.on_trading_rsp_qry_settlement_info(p_api2, obj, bool(double1))
                elif response_type == OnRtnOrder.value:
                    obj = cast(ptr1, POINTER(OrderField)).contents
                    callback.on_trading_rtn_order(p_api2, obj)
                elif response_type == OnRtnTrade.value:
                    obj = cast(ptr1, POINTER(TradeField)).contents
                    callback.on_trading_rtn_trade(p_api2, obj)
                elif response_type == OnRtnQuote.value:
                    obj = cast(ptr1, POINTER(QuoteField)).contents
                    callback.on_trading_rtn_quote(p_api2, obj)
                elif response_type == OnRtnQuoteRequest.value:
                    obj = cast(ptr1, POINTER(QuoteRequestField)).contents
                    callback.on_trading_rtn_quote_request(p_api2, obj)
                elif response_type == OnRspQryHistoricalTicks.value:
                    obj = cast(ptr1, POINTER(TickField)).contents
                    obj2 = cast(ptr2, POINTER(HistoricalDataRequestField)).contents
                    callback.on_trading_rsp_qry_historical_ticks(p_api2, obj, obj2, bool(double1))
                elif response_type == OnRspQryHistoricalBars.value:
                    obj = cast(ptr1, POINTER(BarField)).contents
                    obj2 = cast(ptr2, POINTER(HistoricalDataRequestField)).contents
                    callback.on_trading_rsp_qry_historical_bars(p_api2, obj, obj2, bool(double1))
                elif response_type == OnRspQryInvestor.value:
                    obj = cast(ptr1, POINTER(InvestorField)).contents
                    callback.on_trading_rsp_qry_investor(p_api2, obj)
                elif response_type == OnFilterSubscribe.value:
                    instrument = c_char_p(ptr1).value
                    callback.on_trading_filter_subscribe(p_api2, ExchangeType(double1), size1, size2, size3, instrument)
                elif response_type == OnRtnError.value:
                    obj = cast(ptr1, POINTER(ErrorField)).contents
                    if self._is_market:
                        callback.on_market_rsp_error(p_api2, obj, bool(double1))
                    else:
                        callback.on_trading_rsp_error(p_api2, obj, bool(double1))

    def _on_connect_status(self, p_api, status, p_user_login_field, size):
        """
        callback on connect status
        :param p_api: int
        :param status:
        :param p_user_login_field: POINT of RspUserLoginField
        :return:
        """
        # 连接状态更新
        self.is_connected = Done.value == status

        obj = RspUserLoginField()

        if status in [Logined.value, Disconnected.value, Doing.value] and size > 0:
            obj = cast(p_user_login_field, POINTER(RspUserLoginField)).contents
            self.user_login_field = obj

        if self._callbacks:
            for callback in self._callbacks:
                if self._is_market:
                    callback.on_market_connected(p_api, obj, status)
                else:
                    callback.on_trading_connected(p_api, obj, status)

    def invoke_log(self, func_name, **kwargs):
        for callback in self._callbacks:
            if getattr(callback, func_name, None):
                getattr(callback, func_name)(kwargs)

    def make_response(self, response_type, p_api1=None, p_api2=None, double1=0, double2=0, ptr1=None, size1=0, ptr2=None, size2=0, ptr3=None, size3=0):
        """
        Make a response manually, useful in backtesting class
        :param response_type:
        :param p_api1:
        :param p_api2:
        :param double1:
        :param double2:
        :param ptr1:
        :param size1:
        :param ptr2:
        :param size2:
        :param ptr3:
        :param size3:
        :return:
        """
        if p_api1:
            p_api1 = id(p_api1)
        if p_api2:
            p_api2 = id(p_api2)
        if ptr1:
            ptr1 = byref(ptr1)
            if size1 == 0:
                size1 = 1
        if ptr2:
            ptr2 = byref(ptr2)
            if size2 == 0:
                size2 = 1
        if ptr3:
            ptr3 = byref(ptr3)
            if size3 == 0:
                size3 = 1
        return self._on_response(response_type.value, p_api1, p_api2, double1, double2, ptr1, size1, ptr2, size2, ptr3, size3)