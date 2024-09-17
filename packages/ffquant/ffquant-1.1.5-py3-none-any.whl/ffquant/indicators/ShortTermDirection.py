import backtrader as bt
import os
import pytz
import requests
from datetime import datetime, timedelta
import time

__ALL__ = ['ShortTermDirection']

class ShortTermDirection(bt.Indicator):
    (BEARISH, NA, BULLISH) = (-1, 0, 1)

    lines = ('std',)
    params = (
        ('url', f"{os.environ.get('FINTECHFF_INDICATOR_BASE_URL', 'http://192.168.25.247:8220')}/signal/list"),
        ('symbol', 'CAPITALCOM:HK50'),
        ('backpeek_size', 5),
        ('debug', False)
    )

    def __init__(self):
        self.addminperiod(1)
        self.cache = {}

    def next(self):
        current_bar_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        current_bar_time_str = current_bar_time.strftime('%Y-%m-%d %H:%M:%S')

        if current_bar_time_str not in self.cache or self.cache[current_bar_time_str] == self.NA:
            start_time = current_bar_time - timedelta(minutes=self.p.backpeek_size)
            start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
            end_time = start_time + timedelta(minutes=60)
            end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
            params = {
                'startTime' : start_time_str,
                'endTime' : end_time_str,
                'symbol' : self.p.symbol
            }

            if self.p.debug:
                print(f"ShortTermDirection, fetch data params: {params}")

            response = requests.get(self.p.url, params=params).json()
            if self.p.debug:
                print(f"ShortTermDirection, fetch data response: {response}")

            if response.get('code') != '200':
                raise ValueError(f"API request failed: {response}")
            
            for i in range(0, 60 + self.p.backpeek_size):
                self.cache[(start_time + timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:%S')] = self.NA

            if len(response['results']) > 0:
                for result in response['results']:
                    result_time_str = datetime.fromtimestamp(result['closeTime']/ 1000 - 60).strftime('%Y-%m-%d %H:%M:%S')
                    if result['shortTermDir'] == 'BULLISH':
                        self.cache[result_time_str] = self.BULLISH
                    elif result['shortTermDir'] == 'BEARISH':
                        self.cache[result_time_str] = self.BEARISH

                    if self.p.debug:
                        print(f"ShortTermDirection, result_time_str: {result_time_str}, short_term_dir: {result['shortTermDir']}")
        else:
            if self.p.debug:
                print(f"ShortTermDirection, current_time_str: {current_bar_time_str}, hit cache: {self.cache[current_bar_time_str]}")

        self.lines.std[0] = self.cache.get(current_bar_time_str, self.NA)