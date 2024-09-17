import backtrader as bt
import os
import pytz
import requests
from datetime import datetime, timedelta
import time

__ALL__ = ['LongTermDirection']

class LongTermDirection(bt.Indicator):
    (BEARISH, NA, BULLISH) = (-1, 0, 1)

    lines = ('ltd',)
    params = (
        ('url', f"{os.environ.get('FINTECHFF_INDICATOR_BASE_URL', 'http://192.168.25.247:8220')}/signal/list"),
        ('symbol', 'CAPITALCOM:HK50'),
        ('backpeek_size', 0),
        ('prefetch_size', 60),
        ('debug', False)
    )

    def __init__(self):
        self.addminperiod(1)
        self.cache = {}

    def next(self):
        current_bar_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        current_bar_time_str = current_bar_time.strftime('%Y-%m-%d %H:%M:%S')

        if current_bar_time_str not in self.cache:
            start_time = current_bar_time - timedelta(minutes=self.p.backpeek_size)
            start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
            end_time = start_time + timedelta(minutes=self.p.prefetch_size)
            now = datetime.now().astimezone()
            if end_time > now:
                end_time = now.replace(second=0, microsecond=0)
            end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
            params = {
                'startTime' : start_time_str,
                'endTime' : end_time_str,
                'symbol' : self.p.symbol
            }

            for i in range(0, int((end_time.timestamp() - start_time.timestamp()) / 60 + self.p.backpeek_size)):
                self.cache[(start_time + timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:%S')] = self.NA

            retry_count = 0
            while retry_count < 10:
                retry_count += 1
                if self.p.debug:
                    print(f"LongTermDirection, fetch data params: {params}")

                response = requests.get(self.p.url, params=params).json()
                if self.p.debug:
                    print(f"LongTermDirection, fetch data response: {response}")

                if response.get('code') != '200':
                    raise ValueError(f"API request failed: {response}")

                if len(response['results']) > 0:
                    for result in response['results']:
                        result_time_str = datetime.fromtimestamp(result['closeTime']/ 1000 - 60).strftime('%Y-%m-%d %H:%M:%S')
                        if result['longTermDir'] == 'BULLISH':
                            self.cache[result_time_str] = self.BULLISH
                        elif result['longTermDir'] == 'BEARISH':
                            self.cache[result_time_str] = self.BEARISH

                        if self.p.debug:
                            print(f"LongTermDirection, result_time_str: {result_time_str}, long_term_dir: {result['longTermDir']}")
                    break
                time.sleep(1)
        else:
            if self.p.debug:
                print(f"LongTermDirection, current_time_str: {current_bar_time_str}, hit cache: {self.cache[current_bar_time_str]}")

        self.lines.ltd[0] = self.cache.get(current_bar_time_str, self.NA)
        for i in range(0, self.p.backpeek_size):
            v = self.cache.get((current_bar_time - timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:%S'), self.NA)
            if v != self.NA:
                if self.p.debug:
                    print(f"LongTermDirection, backpeek_size: {i}, v: {v}")
                self.lines.ltd[0] = v
                break