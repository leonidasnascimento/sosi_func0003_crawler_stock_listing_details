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
        next_service_url: str = config_obj.get_value("NEXT_SERVICE_URL")
        func_key_header: str = config_obj.get_value("X_FUNCTION_KEY")

        stock_obj.__dict__ = req.get_json()
        
        logging.info("Crawling the details for '{}'".format(stock_obj.code))
        
        if not (det_crawler.enrich(stock_obj)):
            logging.warning("'{}' was not enriched!".format(stock_obj.code))
        
        logging.info("Calling next function for '{}'".format(stock_obj.code))
        json_obj = json.dumps(stock_obj.__dict__)

        headers = {
            'content-type': "application/json",
            'x-functions-key': func_key_header,
            'cache-control': "no-cache"
        }

        if (next_service_url == ''):
            msg = "No service URL found. {} was processed but no further action was taken. This service is ready for another request.".format(stock_obj.code)

            logging.warning(msg)    
            return func.HttpResponse(body=msg, status_code=200)
        else:
            requests.Response = requests.request("POST", next_service_url, data=json_obj, headers=headers)
            msg = "'{}' was sent to next step. This service is ready for another request".format(stock_obj.code)
            
            logging.info(msg)
            return func.HttpResponse(body=msg, status_code=200)
    except Exception as err:
        logging.error(str(err))
        return func.HttpResponse(body=str(err), status_code=500)
        pass