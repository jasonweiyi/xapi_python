# -*- coding: utf-8 -*-
import unittest
import time
from base.callbacks import CallBacks
from base.comm import get_depth_market_data, get_bid_count, get_bid, get_all_asks, Disconnected
from logger.file_logger import FileLogger
from xapi import XApi, ServerInfoField, UserInfoField

__author__ = 'Chunyou<snowtigersoft@126.com>'


class LtsMarketCallbacks(CallBacks):
    market_data = {}

    def on_market_connected(self, p_api, rsp_user_login, status):
        print "Status: %s" % ord(status)
        if status == Disconnected.value:
            print rsp_user_login.ErrorMsg.decode('gbk')

    def on_market_rtn_depth_market_data_n(self, p_api, p_depth_market_data_n):
        depth_market_data = get_depth_market_data(p_depth_market_data_n)
        if not self.market_data.get(str(depth_market_data.InstrumentID)):
            self.market_data[str(depth_market_data.InstrumentID)] = []
        self.market_data[str(depth_market_data.InstrumentID)].append(depth_market_data)
        print(str(depth_market_data.InstrumentID) + "  " + str(depth_market_data.UpdateTime))
        # 循环获取各买档
        bid_count = get_bid_count(p_depth_market_data_n)
        print u"买档：%s" % bid_count
        for i in range(1, bid_count + 1):
            dp = get_bid(p_depth_market_data_n, i)
            print u"买%s：%s %s" % (i, dp.Price, dp.Size)

        # 一次获取所有卖档数据
        asks = get_all_asks(p_depth_market_data_n)
        print u"卖档：%s" % len(asks)
        for i in range(0, len(asks)):
            dp = asks[i]
            print u"卖%s：%s %s" % (i + 1, dp.Price, dp.Size)

    def on_market_rsp_error(self, p_api, rsp_info, b_is_last):
        print "Error: %s" % rsp_info.ErrorMsg


class LtsMarketTests(unittest.TestCase):
    lts = None
    instrument_ids = [b"600109", b'600601', b'600268', b'600818', b'603997', b'600234']
    exchange_id = b"SSE"

    def setUp(self):
        self.callbacks = [LtsMarketCallbacks(), FileLogger(b"C:/tmp/log")]
        self.lts = XApi("QuantBox_LTS_Quote.dll")
        self.lts.debug = True
        if not self.lts.init():
            print self.lts.get_last_error()
        else:
            server = ServerInfoField()
            server.BrokerID = b"2011"
            server.Address = b"tcp://211.144.195.163:44513"
            server.UserProductInfo = b""
            server.AuthCode = b""

            user = UserInfoField()
            user.UserID = b"020000000352"
            user.Password = b"123"

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

    def test_depth_market_data_single(self):
        self.test_connect()
        self.lts.subscribe(instrument_ids=self.instrument_ids[0], exchange_id=self.exchange_id)
        self.process(10, stop_condition=lambda: len(self.callbacks[0].market_data.get(self.instrument_ids[0], [])) > 10)
        self.lts.unsubscribe(self.instrument_ids[0])
        self.assertNotEqual(len(self.callbacks[0].market_data.get(self.instrument_ids[0], [])), 0, msg='Get Depth Market Data Failed!')

    def test_depth_market_data_multi(self):
        self.test_connect()
        self.lts.subscribe(instrument_ids=self.instrument_ids[:5], exchange_id=self.exchange_id)
        self.process(stop_condition=lambda: len(self.callbacks[0].market_data) > 10)
        self.lts.unsubscribe(self.instrument_ids[:5])
        for ins in self.instrument_ids[:5]:
            self.assertNotEqual(len(self.callbacks[0].market_data.get(ins, [])), 0, msg='Get Depth Market Data for %s Failed!' % ins)


if __name__ == '__main__':
    unittest.main()