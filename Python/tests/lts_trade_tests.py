# -*- coding: utf-8 -*-
import unittest
import time
from base.callbacks import CallBacks
from base.comm import *
from logger.file_logger import FileLogger
from xapi import XApi, ServerInfoField, UserInfoField

__author__ = 'Chunyou<snowtigersoft@126.com>'


class LtsTradeCallbacks(CallBacks):
    trading_account = None
    future_detail = None
    investor_position = None
    order = None
    cancel_order = False

    def on_trading_connected(self, p_api, rsp_user_login, status):
        print "Status: %s" % ord(status)

    def on_trading_rsp_qry_trading_account(self, p_api, trading_account, b_is_last):
        print '\nAccount Info: '
        for k, v in trading_account._fields_:
            print k, getattr(trading_account, k)
        if b_is_last:
            self.trading_account = trading_account

    def on_trading_rsp_error(self, p_api, rsp_info, b_is_last):
        print("Error:" + str(rsp_info.ErrorID) + ", Msg:" + rsp_info.ErrorMsg.decode('gbk'))

    def on_trading_rsp_qry_instrument(self, p_api, instrument, b_is_last):
        """
        请求查询合约响应。当客户端发出请求查询合约指令后，交易托管系统返回响应时，该方法会被调用。
        :param p_api: c_void_p
        :param instrument: InstrumentField
        :param b_is_last: boolean, True if it is the last response for this request
        :return:
        """
        print '\nInstrument: '
        for k, v in instrument._fields_:
            print k, getattr(instrument, k).decode('gbk') if k == 'InstrumentName' else (ord(getattr(instrument, k)) if k in ['Type', 'OptionsType'] else getattr(instrument, k))
        if b_is_last:
            self.future_detail = instrument

    def on_trading_rsp_qry_investor(self, p_api, investor):
        """
        投资者持仓查询应答。当客户端发出投资者持仓查询指令后，后交易托管系统返回响应时，该方法会被调用。
        :param p_api: c_void_p
        :param investor: InvestorField
        :return:
        """
        print '\nInvestor: '
        for k, v in InvestorField._fields_:
            print k, getattr(investor, k)
        self.investor_position = investor

    def on_trading_rtn_order(self, p_api, order):
        """
        报单回报。当客户端进行报单录入、报单操作及其它原因（如部分成交）导致报单状态发生变化时，交易托管系统会主动通知客户端，该方法会被调用。
        :param p_api: c_void_p
        :param order: OrderField
        """
        print '\nOrder: '
        for k, v in order._fields_:
            print k, ":", getattr(order, k).decode('gbk') if k == 'Text' else (ord(getattr(order, k)) if k in ['Type', 'Side', 'OpenClose', 'HedgeFlag', 'TimeInForce', 'Status', 'ExecType'] else getattr(order, k))
        if order.Status in [New.value, PartiallyFilled.value, Filled.value]:
            self.order = order
        elif order.Status in [Cancelled.value]:
            self.cancel_order = True

    def on_trading_rtn_trade(self, p_api, trade):
        """
        成交回报。当发生成交时交易托管系统会通知客户端，该方法会被调用。
        :param p_api: c_void_p
        :param trade:TradeField
        :return:
        """
        print '\nTrade: '
        for k, v in trade._fields_:
            print k, getattr(trade, k)


class LtsTradeTests(unittest.TestCase):
    lts = None
    instrument_ids = [b"600623", b'600601', b'600268', b'600818', b'603997', b'600234']
    exchange_id = b"SSE"

    def setUp(self):
        self.callbacks = [LtsTradeCallbacks(), FileLogger(b"C:/tmp/log")]
        self.lts = XApi("QuantBox_LTS_Trade.dll")
        self.lts.debug = True
        if not self.lts.init():
            print self.lts.get_last_error()
        else:
            server = ServerInfoField()
            server.BrokerID = b"2011"
            server.Address = b"tcp://211.144.195.163:44505"
            server.UserProductInfo = b""
            server.AuthCode = b""

            user = UserInfoField()
            user.UserID = b"020000000352"
            user.Password = b"123321"

            self.lts.connect(b"c:\\tmp\\lts", server, user)
            self.lts.set_callbacks(self.callbacks)

    def tearDown(self):
        self.lts.disconnect()
        self.callbacks[1].flush()

    # 处理消息队列
    def process(self, max_wait=60, stop_condition=lambda: False):
        itr = 0
        while itr < max_wait and not stop_condition():
            itr += 1
            time.sleep(1)

    def test_get_api_name(self):
        self.assertEqual(self.lts.get_api_name(), 'LTS')

    def test_connect(self):
        self.process(5, lambda: self.lts.is_connected)
        self.assertTrue(self.lts.is_connected, msg='Login Failed!')

    def test_get_trading_account(self):
        self.test_connect()
        self.lts.req_qry_trading_account()
        self.process(10, stop_condition=lambda: self.callbacks[0].trading_account is not None)
        self.assertNotEqual(self.callbacks[0].trading_account, None, msg='Get Trading Account Failed!')

    def test_get_future(self):
        self.test_connect()
        self.lts.req_qry_instrument(instrument_id=self.instrument_ids[0], exchange_id=self.exchange_id)
        self.process(stop_condition=lambda: self.callbacks[0].future_detail is not None)
        self.assertNotEqual(self.callbacks[0].future_detail, None, msg='Get Future Failed!')

    def test_get_investor_position(self):
        """
        Works only afer querying trading account or send orders.
        """
        self.test_connect()
        self.lts.req_qry_trading_account()
        self.lts.req_qry_investor_position(instrument_id=self.instrument_ids[0], exchange_id=self.exchange_id)
        self.process(stop_condition=lambda: self.callbacks[0].investor_position is not None)
        self.assertNotEqual(self.callbacks[0].investor_position, None, msg='Get Investor Position info Failed!')

    def test_order(self):
        self.test_connect()
        order = OrderField()
        order.InstrumentID = self.instrument_ids[0]
        order.ExchangeID = self.exchange_id
        order.Type = Limit
        order.Side = Buy
        order.OpenClose = Open
        order.HedgeFlag = Hedge
        order.Qty = 1000
        order.Price = 30
        order.StopPx = 31
        order.TimeInForce = Day
        order_id = create_string_buffer(64)
        self.lts.send_order(order, order_id, 1)
        print "Create Order: %s" % order_id.value
        self.process(stop_condition=lambda: self.callbacks[0].order is not None and self.callbacks[0].order.ID == order_id)
        self.assertNotEqual(self.callbacks[0].order, None, msg='Send Order Failed!')

        cancel_order_id = create_string_buffer(64)
        self.lts.cancel_order(order_id, cancel_order_id, 1)
        print "Cancel Order: %s" % cancel_order_id.value
        self.process(stop_condition=lambda: self.callbacks[0].cancel_order)
        self.assertTrue(self.callbacks[0].cancel_order, msg="Cancel Order Failed")


if __name__ == '__main__':
    unittest.main()