class stock(object):
    """
        Class that represents the 'stock' data model for simple info like 'detail', 'company name' and 'stock code'
    """

    code: str()
    detail: str()
    date_time_operation: str()
    currency: str()
    stock_type: str()
    available_volume: int
    stock_name: str()
    isin_code: str()
    cvm_code: str()

    def __init__(self, code = '', currency = '', stock_type = '', available_volume = 0, stock_name = '', isin_code = '', cvm_code = '', detail = '', dt_operation = ''):
        """
            Class initializer

            Args:
                code = Stock Code
                detail = Extra details that may support the operation
                dt_operation = Date & Time from crawling operation
                currency = Stock currency
                stock_type = Stock type
                available_volume = Available volume for the stock type
        """
        self.code = code
        self.detail = detail
        self.date_time_operation = dt_operation
        self.available_volume = available_volume
        self.stock_type = stock_type
        self.cvm_code = cvm_code
        self.isin_code = isin_code
        self.stock_name = stock_name
        self.currency = currency

        pass
    pass