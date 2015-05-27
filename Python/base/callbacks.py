# -*- coding: utf-8 -*-
__author__ = 'Chunyou<snowtigersoft@126.com>'


class CallBacks:
    """
    The class for all callbacks for both market and trading APIs.
    Sub-class should redefine needed callbacks to implement customized behavior.
    Note:
        1. that some callbacks from the market API and trading API have the same name,
           but we put them into different callbacks. See on_market_connected and on_trading_connected
           as an example.
    """
    def __init__(self):
        pass

    def on_market_connected(self, p_api, rsp_user_login, status):
        """
        callback on market server connect status change
        :param p_api: c_void_p
        :param rsp_user_login: RspUserLoginField
        :param status: ConnectionStatus int
        :return:
        """
        pass

    def on_market_rsp_error(self, p_api, rsp_info, b_is_last):
        """
        callback on market server when error occurred
        :param p_api: c_void_p
        :param rsp_info: ErrorField
        :param b_is_last: boolean, True if it is the last response for this request
        :return:
        """
        pass

    def on_market_rtn_depth_market_data(self, p_api, depth_market_data):
        """
        callback on market server when receive market data
        :param p_api:  c_void_p
        :param depth_market_data: DepthMarketDataField
        :return:
        """
        pass

    def on_trading_connected(self, p_api, rsp_user_login, status):
        """
        callback on trading server connect status change
        :param p_api: c_void_p
        :param rsp_user_login: CThostFtdcRspUserLoginField
        :param status: ConnectionStatus int
        :return:
        """
        pass

    def on_trading_rsp_error(self, p_api, rsp_info, b_is_last):
        """
        callback on trading server when error occurred
        :param p_api: c_void_p
        :param rsp_info: CThostFtdcRspInfoField
        :param b_is_last: boolean, True if it is the last response for this request
        :return:
        """
        pass

    def on_trading_rsp_qry_depth_market_data(self, p_api, depth_market_data, rsp_info, b_is_last):
        """
        请求查询行情响应。当客户端发出请求查询行情指令后，交易托管系统返回响应时，该方法会被调用。
        :param p_api: c_void_p
        :param depth_market_data: CThostFtdcDepthMarketDataField
        :param rsp_info: CThostFtdcRspInfoField
        :param b_is_last: boolean, True if it is the last response for this request
        :return:
        """
        pass

    def on_trading_rsp_qry_instrument(self, p_api, instrument, b_is_last):
        """
        请求查询合约响应。当客户端发出请求查询合约指令后，交易托管系统返回响应时，该方法会被调用。
        :param p_api: c_void_p
        :param instrument: InstrumentField
        :param b_is_last: boolean, True if it is the last response for this request
        :return:
        """
        pass

    def on_trading_rsp_qry_investor_position(self, p_api, investor_position, b_is_last):
        """
        投资者持仓查询应答。当客户端发出投资者持仓查询指令后，后交易托管系统返回响应时，该方法会被调用。
        :param p_api: c_void_p
        :param investor_position: PositionField
        :param b_is_last: boolean, True if it is the last response for this request
        :return:
        """
        pass

    def on_trading_rsp_qry_trading_account(self, p_api, trading_account, b_is_last):
        """
        请求查询资金账户响应。当客户端发出请求查询资金账户指令后，交易托管系统返回响应时，该方法会被调用。
        :param p_api: c_void_p
        :param trading_account: AccountField
        :param b_is_last: boolean, True if it is the last response for this request
        :return:
        """
        pass

    def on_trading_rsp_qry_settlement_info(self, p_api, settlement_info, b_is_last):
        """
        请求查询结算信息响应。当客户端发出请求查询结算信息指令后，交易托管系统返回响应时，该方法会被调用。
        :param p_api: c_void_p
        :param settlement_info: SettlementInfoField
        :param b_is_last: boolean, True if it is the last response for this request
        :return:
        """
        pass

    def on_trading_rtn_order(self, p_api, order):
        """
        报单回报。当客户端进行报单录入、报单操作及其它原因（如部分成交）导致报单状态发生变化时，交易托管系统会主动通知客户端，该方法会被调用。
        :param p_api: c_void_p
        :param order: OrderField
        """
        pass

    def on_trading_rtn_trade(self, p_api, trade):
        """
        成交回报。当发生成交时交易托管系统会通知客户端，该方法会被调用。
        :param p_api: c_void_p
        :param trade:TradeField
        :return:
        """
        pass

    def on_trading_rtn_quote(self, p_api, quote):
        """
        Quote
        :param p_api: c_void_p
        :param quote: QuoteField
        """
        pass

    def on_trading_rtn_quote_request(self, p_api, quote_request):
        """
        Quote Request
        :param p_api: c_void_p
        :param quote_request: QuoteRequestField
        """
        pass

    def on_trading_rsp_qry_historical_ticks(self, p_api, tick, historical_data_request, b_is_last):
        """
        Historical Data
        :param p_api:
        :param tick: TickField
        :param historical_data_request: HistoricalDataRequestField
        :param b_is_last:
        :return:
        """
        pass

    def on_trading_rsp_qry_historical_bars(self, p_api, bar, historical_data_request, b_is_last):
        """
        Historical Data
        :param p_api:
        :param bar: BarField
        :param historical_data_request: HistoricalDataRequestField
        :param b_is_last:
        :return:
        """
        pass

    def on_trading_rsp_qry_investor(self, p_api, investor):
        """
        Qry investor
        :param p_api:
        :param investor:
        :return:
        """
        pass

    def on_trading_filter_subscribe(self, p_api, exchange, instrument_part1, instrument_part2, instrument_part3, pInstrument):
        """
        Filter Subscribe
        :param p_api:
        :param exchange:
        :param instrument_part1:
        :param instrument_part2:
        :param instrument_part3:
        :param pInstrument:
        :return:
        """
        pass