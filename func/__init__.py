import logging
import azure.functions as func
import json
import requests
import pathlib

from .models.stock import stock
from .crawler import stock_code_details_crawler
from configuration_manager.reader import reader

SETTINGS_FILE_PATH = pathlib.Path(__file__).parent.parent.__str__() + "//local.settings.json"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('sosi_func0003_crawler_stock_listing_details function processed a request.')

    try:
        stock_obj: stock = stock()
        det_crawler: stock_code_details_crawler = stock_code_details_crawler()
        config_obj = reader(SETTINGS_FILE_PATH, "Values")

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

        url_to_call = config_obj.get_value("NEXT_SERVICE_TO_CALL")

        if (url_to_call == ''):
            msg = "There was not a service URL to call, so no action was taken. This service is ready for another request."

            logging.warning(msg)    
            return func.HttpResponse(body=msg, status_code=200)
        else:
            requests.Response = requests.request("POST", url_to_call, data=json_obj, headers=headers)
            msg = "'{}' was sent to next step. This service is ready for another request".format(stock_obj.code)
            
            logging.info(msg)
            return func.HttpResponse(body=msg, status_code=200)
    except Exception as err:
        logging.error(str(err))
        return func.HttpResponse(body=str(err), status_code=500)
        pass