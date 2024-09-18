import pandas as pd
from .exceptions import APIError
from .utils import format_response, validate_stock_symbol
import requests
import logging

logger = logging.getLogger(__name__)


class ZhiSQuant_SDK:
    def __init__(self, base_url=None, api_key=None):
        self.base_url = base_url or 'http://47.122.29.249:8080'
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        logger.debug(f"Initialized ZhiSQuant_SDK with base_url={self.base_url}")

    def get_stock_data(self, stock_symbol: str) -> pd.DataFrame:
        validate_stock_symbol(stock_symbol)
        url = f"{self.base_url}/stocks/{stock_symbol}"
        logger.debug(f"Requesting URL: {url}")
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = format_response(response)
            df = pd.DataFrame([data])
            logger.debug(f"Received data: {df}")
            return df
        else:
            logger.error(f"API request failed with status code {response.status_code}: {response.text}")
            raise APIError(f"API request failed with status code {response.status_code}: {response.text}")

    def get_all_stocks(self) -> pd.DataFrame:
        url = f"{self.base_url}/stocks"
        logger.debug(f"Requesting URL: {url}")
        response = requests.post(url, headers=self.headers)
        if response.status_code == 200:
            data = format_response(response)
            df = pd.DataFrame(data)
            logger.debug(f"Received data: {df}")
            return df
        else:
            logger.error(f"API request failed with status code {response.status_code}: {response.text}")
            raise APIError(f"API request failed with status code {response.status_code}: {response.text}")
