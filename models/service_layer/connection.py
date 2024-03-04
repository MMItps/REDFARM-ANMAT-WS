import httpx
from pydantic import BaseModel
from typing import Union
from jinja2 import Environment, FileSystemLoader
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta


load_dotenv()

HOST= os.environ.get("HOST")
COMPANY_DB = os.environ.get("COMPANY_DB")
USERNAME_SAP=os.environ.get("USERNAME_SAP")
PASSWORD_SAP=os.environ.get("PASSWORD_SAP")

class ConnectionServiceLayer(BaseModel):
    host: str = HOST
    user: str = USERNAME_SAP
    password: str = PASSWORD_SAP
    company_db: str = COMPANY_DB
    sessionID: dict = ""
    sessionTime: datetime = ""


    def _validate_session(self):
        delta_time = datetime.now() - self.sessionTime

        if delta_time > timedelta(minutes=30):
            self.login()

    async def login(self):
        try:
            async with httpx.AsyncClient(base_url=self.host) as client:
                login_data = {
                    "CompanyDB": self.company_db,
                    "UserName": self.user,
                    "Password": self.password
                }
                response = await client.post(url="/Login",content=login_data, timeout=60)
                
                if response.status_code == 200:
                    self.sessionTime = datetime.now()
                    self.sessionID = {"B1SESSION": response.content["SessionId"]}
                else:
                    raise Exception("Error al iniciar session")
        except Exception as e:
            print(f"Error: {e}")
            pass

    async def get_info(self, endpoint="", select="", filters="", order=""):
        try:
            self._validate_session()
            params= {}
            if select != "": params.update({'$select': select})
            if filters != "": params.update({'$filter': filters})
            if order != "": params.update({'$orderby': order})
            
            async with httpx.AsyncClient(base_url=self.host, cookies=self.sessionID) as client:
                response = await client.get(url=endpoint, params=params)

                if response.status_code == 200:
                    return response.content
                else: 
                    raise Exception(f"Error requests: Status Code: {response.status_code} Message: {response.content}")
        except Exception as e:
            print(e)
    
    async def post_info(self, endpoint, body):
        try:
            self._validate_session()
            async with httpx.AsyncClient(base_url=self.host, cookies=self.sessionID) as client:
                response = await client.post(url=endpoint, content=body)

                if response.status_code == 201:
                    return response.content
                else: 
                    raise Exception(f"Error requests: Status Code: {response.status_code} Message: {response.content}")

        except Exception as e:
            print(e)