import httpx
from pydantic import BaseModel
from typing import Union
from jinja2 import Environment, FileSystemLoader
import xmltodict
import xml.etree.ElementTree as ET

folder_template = Environment(loader=FileSystemLoader('template'))

class HttpxConnection(BaseModel):
    base_url: str = "https://servicios.pami.org.ar"
    ws_user: str = "testwservice"
    ws_pass: str = "testwservicepsw"

    async def send_requests(self, body:str):

        main_template = folder_template.get_template("main.xml")
        soap_body = main_template.render(Body=body)

        async with httpx.AsyncClient(base_url=self.base_url) as client:
            response = await client.post(url="/trazamed.WebService",content=soap_body, timeout=60)
            
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                ns1_element = root.findall('.//ns1:*', namespaces={'ns1': 'http://business.mywebservice.inssjp.com/'})
                result = ET.tostring(ns1_element[0][0]).decode()
                data_to_dict = xmltodict.parse(result)
                return data_to_dict
            else:
                return False

