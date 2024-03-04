import anyio
import asyncer
import time
import json
from models.ws_anmat.connection import HttpxConnectionTest
from models.ws_anmat.ws_method import GetCatalogoByGLN

CONN = HttpxConnectionTest()

async def fetch_to_ws(page=1, gln="", cuit=""):
    try:
        result = await GetCatalogoByGLN(Page=page, CUIT=cuit).send_to_ws(CONN)

        if result['return'] == None:
            return False
        if type(result['return']['list']) == list:
            return result['return']['list'][0]
        return result['return']['list']
    
    except:
        pass

async def get_data_cuit(cuit_list=[]):
    try:
        async with asyncer.create_task_group() as task_group:
            tasks = [task_group.soonify(fetch_to_ws)(cuit=cuit) for cuit in cuit_list]

        tasks = [v.value for v in tasks]

        if False in tasks:
            return tasks, True
            
        return tasks, False
    except:
        pass

async def cuit_list_process(cuit_list, step=20):
    try:
        dicc = {}
        sub_group = [cuit_list[i:i+step] for i in range(0, len(cuit_list), step)]
        
        for group in sub_group:
            data, err = await get_data_cuit(group)
            #[dicc.update(format_dicc(v)) for v in data if v != False]        
        return data
    
    except:
        pass

async def filter_baja(data_list):
    
    def _filter_baja(value):
        baja = value.get('email', None)
        if baja: 
            return baja
        else: 
            return None

    try:
        result = list(map(_filter_baja, data_list))
        return result
        
    except:
        pass


async def start_process():
    
    try:
        cuit_list = ["23269267879", "20259171289", "27936035189", "27123497851", "27123552828"]
        result = await cuit_list_process(cuit_list)
        bajas = await filter_baja(result)

    except:
        pass


if __name__ == "__main__":
    inicio = time.time()
    anyio.run(start_process)
    fin = time.time()
    tiempo_ejecucion = fin - inicio
    print("Tiempo de ejecución:", tiempo_ejecucion, "segundos")