"""Crawls the poloniex API"""
import logging
import os

import requests

LOGGER = None
API = 'https://ftx.com/api/markets/'
START_TIME = 1495032490  # Wednesday, May 17, 2017 4:48:10 PM GMT+02:00
END_TIME = 1652798890  # Tuesday, May 17, 2022 4:48:10 PM GMT+02:00
INPUT_FIELDS = {
    'resolution': 15,  # every X sec
    'start_time': None,
    'end_time': None
}
FILE_SIZE = 10000
CURRENCIES = [
    'BTC/USDT',
    'ETH/USDT',
    'BNB/USDT',
    'XRP/USDT',
    'ADA/USDT',
    'SOL/USDT',
    'DOGE/USDT',
    'DOT/USDT',
    'AVAX/USDT',
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
        _currentCurrency = currency
        _previous_interval = -1

        # loop over start to end time with step size (file_size*resolution)
        _time_intervals = range(START_TIME, END_TIME,
                                FILE_SIZE * INPUT_FIELDS['resolution'])
        for idx, interval in enumerate(_time_intervals):

            # skip first range return
            if _previous_interval < 0:
                _previous_interval = interval
                continue

            LOGGER.debug(
                f'Current Interval: {_previous_interval}/{interval} --- {idx}/{len(_time_intervals)}'
            )

            INPUT_FIELDS['start_time'] = _previous_interval
            INPUT_FIELDS['end_time'] = interval

            historicalAPI = API + _currentCurrency + '/candles?'
            # get request
            response = requests.get(historicalAPI, params=INPUT_FIELDS)

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
