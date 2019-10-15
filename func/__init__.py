import logging
import azure.functions as func
import json
import requests

from .models.stock import stock
from .crawler import stock_code_details_crawler

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('sosi_func0003_crawler_stock_listing_details function processed a request.')

    try:
        stock_obj: stock = stock()
        det_crawler: stock_code_details_crawler = stock_code_details_crawler()

        stock_obj.__dict__ = req.get_json()
        
        logging.info("Crawling the details for '{}'".format(stock_obj.code))
        det_crawler.enrich(stock_obj)
        
        logging.info("Calling next function for '{}'".format(stock_obj.code))
        json_obj = json.dumps(stock_obj.__dict__)

        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "652ec406-7b16-40ca-8436-5baf1d36b793"
        }

        response: requests.Response = requests.request("POST", "**LINK_HERE**", data=json_obj, headers=headers)

    except ValueError:
        pass
