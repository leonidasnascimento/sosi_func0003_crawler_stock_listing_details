import urllib3
import datetime

from typing import List
from .models.stock import stock
from bs4 import (BeautifulSoup, ResultSet)

class stock_code_details_crawler():
    stock_det_url = "https://br.advfn.com/bolsa-de-valores/bovespa/{}/cotacao"
      
    def __init__(self):
        pass

    def enrich(self, stock_ref: stock) -> bool:
        url_det = str(self.stock_det_url).format(stock_ref.code)
        req = urllib3.PoolManager()
        res = req.request('GET', url_det)
        soup = BeautifulSoup(res.data, 'html.parser')
        divs_details = soup.find_all('div', {'class': 'TableElement'})

        if (not (divs_details is None)) and len(divs_details) > 0:
            div_1_det = divs_details[0].find('table').findAll('td')
            div_2_det = divs_details[2].find('table').findAll('td')
            
            stock_ref.detail = div_1_det[len(div_1_det) - 1].text
            stock_ref.stock_name = div_1_det[0].text
            stock_ref.isin_code = div_1_det[4].text
            stock_ref.stock_type = self.__set_stock_type(div_1_det[3].text)
            stock_ref.currency = 'BRL' # div_2_det[len(div_2_det) - 1].text

            return True

        return False
    
    def __set_stock_type(self, stock_type: str):
        if stock_type.lower() == 'preferencial':
            return 'PN'
        else:
            if stock_type.lower() == 'ordinária':
                return 'ON'
            else:
                return stock_type
        pass
    pass