import httpx
import asyncio
from pydantic import BaseModel
import json
import time

class HttpxConnectionService(BaseModel):
    base_url: str = "http://127.0.0.1:8000/"
    ws_user: str = "9990664100004"
    ws_pass: str = "Pami1111"

    async def send_requests(self, page:int=1):
        body = {
                "User": self.ws_user,
                "Password": self.ws_pass,
                "GLN": "",
                "CUIT": "",
                "Razon_social": "",
                "Id_prov": "",
                "Page": page,
                "Offset": 100
                }
        timeout = httpx.Timeout(30.0) 
        async with httpx.AsyncClient(base_url=self.base_url,timeout=timeout) as client:
            response = await client.post(url="/anmat/get_catalogo_gln",json=body)
            
            if response.status_code == 200:
                return response.json()["list"]
            else:
                return False

Conn = HttpxConnectionService()

async def fetch_page(page):
    result = await Conn.send_requests(page=page)
    if result:
        return result
    return False

def format_values(lista):
    lista = {v['gln']: v for v in lista if "cuit" in v}
    return lista
            
async def main():
    page = 1
    result = {}
    while True:
        response = await fetch_page(page)

        if not response:
            break
        result.update(format_values(response))
        page += 1
    # Guardar el resultado en un archivo JSON
    with open("result.json", "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

    print(page)
    print(len(result))

if __name__ == "__main__":
    inicio = time.time()
    asyncio.run(main())
    fin = time.time()
    delta = fin - inicio

    print(delta)