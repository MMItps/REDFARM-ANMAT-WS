import httpx
from pydantic import BaseModel
from typing import Union
from jinja2 import Environment, FileSystemLoader
import xmltodict
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv


load_dotenv()

folder_template = Environment(loader=FileSystemLoader('template'))

BASE_URL_TEST = os.environ.get("baseURLTest")
WS_USER_TEST = os.environ.get("ws_user_test")
WS_PASS_TEST = os.environ.get("ws_pass_test")
USER_TEST = os.environ.get("UserTest")
PASS_TEST = os.environ.get("PassTest")

BASE_PATH = os.environ.get("basePath")

BASE_URL = os.environ.get("baseURLProd")
USER = os.environ.get("UserProd")
PASS = os.environ.get("PassProd")
WS_USER = os.environ.get("ws_user_prod")
WS_PASS = os.environ.get("ws_pass_prod")

class HttpxConnection(BaseModel):

    async def send_requests(self, body:str):

        main_template = folder_template.get_template("main.xml")
        soap_body = main_template.render(Body=body, User=self.ws_user,Credential=self.ws_pass)

        try:
            async with httpx.AsyncClient(base_url=self.base_url) as client:

                response = await client.post(url=BASE_PATH,content=soap_body, timeout=60)
                
                if response.status_code == 200:
                    root = ET.fromstring(response.text)
                    ns1_element = root.findall('.//ns1:*', namespaces={'ns1': 'http://business.mywebservice.inssjp.com/'})
                    result = ET.tostring(ns1_element[0][0]).decode()
                    data_to_dict = xmltodict.parse(result)
                    return data_to_dict
                else:
                    return False
        except:
            pass

class HttpxConnectionTest(HttpxConnection):
    base_url: str = BASE_URL_TEST
    ws_user: str = WS_USER_TEST
    ws_pass: str = WS_PASS_TEST



class HttpxConnectionProd(HttpxConnection):
    base_url: str = BASE_URL
    ws_user: str = WS_USER
    ws_pass: str = WS_PASS
