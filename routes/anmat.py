from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from models.ws_anmat.ws_method import *

anmat = APIRouter(prefix="/anmat", tags=["Anmat"])

@anmat.post(
    path="/no_confirm",
    status_code=200
    )
async def Handler_GetNoConfirm(
    get_no_confirm: GetNoConfirm = Body()
    ):
    """
    Description:
    - **Items 1** 
    """
    ws_client = HttpxConnection()
    response = await get_no_confirm.send_to_ws(ws_client)
    
    if response:
        error = response['return'].get("errores", None)
        if error: return JSONResponse(content=error, status_code=400)
        
        return JSONResponse(content=response["return"])
    
    return JSONResponse(content={"status": "Error", "message":"Error format xml"}, status_code=400)

@anmat.post(
    path="/get_catalogo_gln",
    status_code=200
    )
async def Handler_GetCatalogoGln(
    get_catalogo: GetCatalogoByGLN = Body()
    ):
    """
    Description:
    - **Items 1** 
    """
    ws_client = HttpxConnection()
    response = await get_catalogo.send_to_ws(ws_client)
    
    if response:
        if response['return'] == None:
            return JSONResponse(content={"status": "Not Found", "message":"No existe GLN en el catalogo"}, status_code=404)
        error = response['return'].get("errores", None)
        if error: return JSONResponse(content=error, status_code=400)

        print(response)
        return JSONResponse(content=response["return"])
    
    return JSONResponse(content={"status": "Error", "message":"Error format xml"}, status_code=400)


@anmat.post(
    path="/confirm",
    status_code=200
    )
async def Handler_Confirm(
    confirm: Confirm = Body()
    ):
    """
    Description:
    - **Items 1** 
    """
    ws_client = HttpxConnection()
    response = await confirm.send_to_ws(ws_client)
    
    if response:
        error = response['return'].get("errores", None)
        if error: return JSONResponse(content=error, status_code=400)
        
        return JSONResponse(content=response["return"])
    
    return JSONResponse(content={"status": "Error", "message":"Error format xml"}, status_code=400)


@anmat.post(
    path="/cancel",
    status_code=200
    )
async def Handler_Cancel(
    cancel: Cancel = Body()
    ):
    """
    Description:
    - **Items 1** 
    """
    ws_client = HttpxConnection()
    response = await cancel.send_to_ws(ws_client)

    if response:
        error = response['return'].get("errores", None)
        if error: return JSONResponse(content=error, status_code=400)
        
        return JSONResponse(content=response["return"])
    
    return JSONResponse(content={"status": "Error", "message":"Error format xml"}, status_code=400)


@anmat.post(
    path="/sendMed",
    status_code=200
    )
async def Handler_SendMedicamento(
    send_medicamentos: SendMedicamento = Body()
    ):
    """
    Description:
    - **Items 1** 
    """
    ws_client = HttpxConnection()
    response = await send_medicamentos.send_to_ws(ws_client)
    
    if response:
        error = response['return'].get("errores", None)
        if error: return JSONResponse(content=error, status_code=400)
        
        return JSONResponse(content=response["return"])
    
    return JSONResponse(content={"status": "Error", "message":"Error format xml"}, status_code=400)

