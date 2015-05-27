# -*- coding: utf-8 -*-
__author__ = 'Chunyou<snowtigersoft@126.com>'

import os
import codecs
import json
from datetime import datetime
from .logger import Logger


class FileLogger(Logger):
    """
    A file based CTP logger.
    """

    def __init__(self, folder, append=True, in_memory_records=1000, datetime_format='%Y-%m-%d %H:%M:%S',
                 datetime_adapter=None):
        """
        Initialize current logger.
        :param folder: string. folder of the log files. The folder will have the following sub-folders:
            (1) market, this folder stores depth market data from the marketing api.
            (2) trading, this folder stores all the other kinds of data.
            In each folder, the should be files yyyy-mm-dd.txt for each day.
        :param in_memory_records, int, the maximal number of log records to keep in memory
            before flushing them into the log file.
        :param append: boolean, if True and if a log file exists, append to that file;
            otherwise empty the existing log file.
        :param datetime_format: string, datetime format in the log file.
        :param datetime_adapter: function pointer from datetime to datetime, used to adapt time in different time zones.
        """
        Logger.__init__(self)
        self.append = append
        self.datetime_format = datetime_format
        self.market_folder = folder + os.path.sep + 'market'
        self._mkdir(self.market_folder)
        self.trading_folder = folder + os.path.sep + 'trading'
        self._mkdir(self.trading_folder)
        self.in_memory_records = in_memory_records
        self.datetime_adapter = datetime_adapter

    @classmethod
    def _mkdir(cls, newdir):
        """works the way a good mkdir should :)
            - already exists, silently complete
            - regular file in the way, raise an exception
            - parent directory(ies) does not exist, make them as well
        """
        if os.path.isdir(newdir):
            pass
        elif os.path.isfile(newdir):
            raise OSError("a file with the same name as the desired " \
                          "dir, '%s', already exists." % newdir)
        else:
            head, tail = os.path.split(newdir)
            if head and not os.path.isdir(head):
                cls._mkdir(head)
            if tail:
                os.mkdir(newdir)

    def flush_impl(self):
        filename = datetime.now().strftime('%Y-%m-%d.txt')

        # flush trading data
        handle = codecs.open(self.trading_folder + os.path.sep + filename, 'a' if self.append else 'w', 'utf-8')
        trading_data, self.trading_data = self.trading_data, []
        for item in trading_data:
            handle.write("%s\t%s\t%s\n" % (
                item[0].strftime(self.datetime_format), item[1], json.dumps(item[2], ensure_ascii=False)))
        handle.close()

        # flush market data
        handle = codecs.open(self.market_folder + os.path.sep + filename, 'a' if self.append else 'w', 'utf-8')
        market_data, self.market_data = self.market_data, []
        for item in market_data:
            handle.write("%s\t%s\t%s\n" % (
                item[0].strftime(self.datetime_format), item[1], json.dumps(item[2], ensure_ascii=False)))
        handle.close()