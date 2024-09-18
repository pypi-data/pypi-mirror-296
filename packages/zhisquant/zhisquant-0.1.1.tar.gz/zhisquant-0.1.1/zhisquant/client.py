import requests
import pandas as pd
from .exceptions import APIError
from .utils import format_response, validate_stock_symbol
import logging

logger = logging.getLogger(__name__)


class ZhiSQuant_SDK:
    def __init__(self, base_url=None, api_key=None):
        self.base_url = base_url or 'http://47.122.29.249:8080'
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        logger.debug(f"Initialized ZhiSQuant_SDK with base_url={self.base_url}")

    def get_stock_price(self, stock, col_names, start_date, end_date):
        """
        获取单个股票的价格数据
        Args:
            stock (str): 股票代码
            col_names (list): 需要获取的字段列表
            start_date (str): 开始日期，格式 'YYYY-MM-DD'
            end_date (str): 结束日期，格式 'YYYY-MM-DD'
        Returns:
            pd.DataFrame: 股票价格数据
        """
        validate_stock_symbol(stock)
        url = f"{self.base_url}/stock_price"
        params = {
            "stock": stock,
            "columns": ','.join(col_names),
            "start_date": start_date,
            "end_date": end_date
        }
        logger.debug(f"Requesting URL: {url} with params: {params}")
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json().get('data')
            df = pd.DataFrame(data)
            logger.debug(f"Received data: {df}")
            return df
        else:
            logger.error(f"API请求失败，状态码: {response.status_code}, 错误信息: {response.text}")
            raise APIError(f"API请求失败，状态码: {response.status_code}, 错误信息: {response.text}")

    def get_stock_income_data(self, stock_codes, column_names, start_date, end_date):
        """
        获取股票的财务收入数据（利润表）
        """
        return self._get_finance_data(stock_codes, column_names, start_date, end_date, table_name='income', Type=1)

    def get_stock_balance_data(self, stock_codes, column_names, start_date, end_date):
        """
        获取股票的资产负债表数据
        """
        return self._get_finance_data(stock_codes, column_names, start_date, end_date, table_name='balance', Type=1)

    def get_stock_finance_data(self, stock_codes, column_names, start_date, end_date):
        """
        获取股票的主要财务指标数据
        """
        return self._get_finance_data(stock_codes, column_names, start_date, end_date, table_name='main_finance')

    def get_stock_cashflow_data(self, stock_codes, column_names, start_date, end_date):
        """
        获取股票的现金流量表数据
        """
        return self._get_finance_data(stock_codes, column_names, start_date, end_date, table_name='cash_flow')

    def _get_finance_data(self, stock_codes, column_names, start_date, end_date, table_name, Type=None):
        """
        通用方法，用于获取财务数据
        """
        url = f"{self.base_url}/finance_data/{table_name}"
        params = {
            "stock_codes": ','.join(stock_codes) if isinstance(stock_codes, list) else stock_codes,
            "columns": ','.join(column_names),
            "start_date": start_date,
            "end_date": end_date
        }
        if Type is not None:
            params["Type"] = Type
        logger.debug(f"Requesting URL: {url} with params: {params}")
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json().get('data')
            df = pd.DataFrame(data)
            logger.debug(f"Received data: {df}")
            return df
        else:
            logger.error(f"API请求失败，状态码: {response.status_code}, 错误信息: {response.text}")
            raise APIError(f"API请求失败，状态码: {response.status_code}, 错误信息: {response.text}")
