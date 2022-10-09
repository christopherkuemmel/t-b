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
"""Crawls the poloniex API"""
import logging
import os

import requests

LOGGER = None
API = 'https://poloniex.com/public'
START_TIME = 1495032490  # Wednesday, May 17, 2017 4:48:10 PM GMT+02:00
END_TIME = 1652798890  # Tuesday, May 17, 2022 4:48:10 PM GMT+02:00
INPUT_FIELDS = {
    'command': 'returnChartData',
    'period': 300,  # every X sec
    'currencyPair': '',
    'start': None,
    'end': None
}
FILE_SIZE = 10000
CURRENCIES = [
    'USDT_BTC',
    'USDT_ETH',
    'USDT_BNB',
    'USDT_XRP',
    'USDT_ADA',
    'USDT_SOL',
    'USDT_DOGE',
    'USDT_DOT',
    'USDT_AVAX',
]


def create_logger(output_path: str = './data/crawl') -> logging.Logger:
    """Creates and returns a logger.

    Args:
        output_path(str): The path to the log file.

    Returns:
        logging.logger: The logger.
    """
    # create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # create output dir
    if not os.path.exists(output_path):
        try:
            os.makedirs(output_path)
        except:
            logger.error("Error while try to create directory for logger.")
    # create file handler which logs even debug messages
    fh = logging.FileHandler(os.path.join(output_path, 'log.log'))
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '{asctime} - {name} - {levelname} - {message}', style='{')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def crawl():
    """Crawls the API, requests, receives and saves the currency information."""

    # loop over defined currencies
    for currency in CURRENCIES:

        LOGGER.debug(f'Start crawling {currency}')

        # set currency
        INPUT_FIELDS['currencyPair'] = currency
        _previous_interval = -1

        # loop over start to end time with step size (file_size*period)
        _time_intervals = range(START_TIME, END_TIME,
                                FILE_SIZE * INPUT_FIELDS['period'])
        for idx, interval in enumerate(_time_intervals):

            # skip first range return
            if _previous_interval < 0:
                _previous_interval = interval
                continue

            LOGGER.debug(
                f'Current Interval: {_previous_interval}/{interval} --- {idx}/{len(_time_intervals)}'
            )

            INPUT_FIELDS['start'] = _previous_interval
            INPUT_FIELDS['end'] = interval

            # get request
            response = requests.get(API, params=INPUT_FIELDS)

            # create file and dir
            _filename = f'./data/crawl/{currency}/{_previous_interval}-{interval}.json'
            # LOGGER.debug(f'Create FILE: {_filename}')
            os.makedirs(os.path.dirname(_filename), exist_ok=True)

            # write file
            with open(_filename, 'w+', encoding='utf-8') as json_file:
                json_file.writelines(response.content.decode("utf-8"))

            _previous_interval = interval


if __name__ == "__main__":
    LOGGER = create_logger()
    crawl()
