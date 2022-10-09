# -*- coding: utf-8 -*-
# Copyright 2022 Christopher Kümmel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This module contains the class for requesting crypto data from exchanges."""
import json

import pandas as pd
import requests
from tqdm import tqdm


class CryptoDataRequest:
    """CryptoDataRequest"""

    def __init__(self):
        self.ftx_url = 'https://ftx.com/api/markets/'
        self.poloniex_url = 'https://api.poloniex.com/markets/'
        self.max_request_interval = 300

    def _request_poloniex(self, currency: str, start_date: int, end_date: int,
                          resolution: int) -> pd.DataFrame:
        """https://docs.poloniex.com/#public-endpoints-market-data-candles"""
        input_fields = {
            'interval':
            'MINUTE_' + str(resolution // 60),  # TODO: fix interval for hours
            'limit': self.max_request_interval,
        }
        historical_api = self.poloniex_url + currency + '/candles'

        crypto_data = []
        _previous_interval = -1
        for interval in tqdm(
                range(start_date * 1000, end_date * 1000,
                      resolution * self.max_request_interval * 1000)):

            # skip first range return
            if _previous_interval < 0:
                _previous_interval = interval
                continue

            input_fields['startTime'] = _previous_interval
            input_fields['endTime'] = interval

            # get request
            response = requests.get(historical_api, params=input_fields)
            if response.status_code == 200:
                crypto_data.extend(json.loads(response.content.decode("utf-8")))

            _previous_interval = interval

        columns = [
            'low', 'high', 'open', 'close', 'amount', 'quantity',
            'buyTakerAmount', 'buyTakerQuantity', 'tradeCount', 'ts',
            'weightedAverage', 'interval', 'startTime', 'closeTime'
        ]
        return pd.DataFrame(crypto_data, columns=columns)

    def _request_ftx(self, currency: str, start_date: int, end_date: int,
                     resolution: int) -> pd.DataFrame:
        """https://docs.ftx.com/#get-historical-prices"""
        input_fields = {
            'resolution': resolution,
        }
        historical_api = self.ftx_url + currency + '/candles'

        crypto_data = []
        _previous_interval = -1
        for interval in tqdm(
                range(start_date, end_date,
                      resolution * self.max_request_interval)):

            # skip first range return
            if _previous_interval < 0:
                _previous_interval = interval
                continue

            input_fields['start_time'] = _previous_interval
            input_fields['end_time'] = interval

            # get request
            response = requests.get(historical_api, params=input_fields)
            if response.status_code == 200:
                crypto_data.extend(
                    json.loads(response.content.decode("utf-8"))['result'])

            _previous_interval = interval
        return pd.DataFrame(crypto_data)

    def request(self,
                currency: str,
                start_date: int,
                end_date: int,
                exchange: str = 'ftx',
                resolution: int = 300,
                file_path: str = None) -> pd.DataFrame:
        """
        Args:
        Returns:
        Raises:
        """
        if exchange == 'ftx':
            crypto_df = self._request_ftx(currency, start_date, end_date,
                                          resolution)
        elif exchange == 'poloniex':
            crypto_df = self._request_poloniex(currency, start_date, end_date,
                                               resolution)
        else:
            raise NotImplementedError

        if file_path:
            crypto_df.to_csv(file_path, sep=',')

        return crypto_df
