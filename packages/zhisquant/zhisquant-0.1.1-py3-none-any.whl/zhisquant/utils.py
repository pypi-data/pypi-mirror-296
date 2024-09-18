def format_response(response):
    json_data = response.json().get('data')
    if json_data and 'previous_data' in json_data:
        del json_data['previous_data']
    return json_data


def validate_stock_symbol(symbol):
    if not isinstance(symbol, str) or not symbol:
        raise ValueError("Stock symbol must be a non-empty string.")
