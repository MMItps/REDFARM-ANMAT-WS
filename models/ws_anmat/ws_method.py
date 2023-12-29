from datetime import datetime
from enum import IntEnum
from pydantic import BaseModel
from typing import Optional, Union
from jinja2 import Environment, FileSystemLoader
from models.ws_anmat.connection import HttpxConnection


folder_template = Environment(loader=FileSystemLoader('template'))

class CredentialUser(BaseModel):
    User: Optional[str]= "9990664100004"
    Password: Optional[str]= "Pami1111"

class Cancel(CredentialUser):
    ID: Union[int, str] 

    async def send_to_ws(self, connection: HttpxConnection):
        cancel_template = folder_template.get_template("sendCancelTrans.xml")
        cancel_template = cancel_template.render(data=self)
        response = await connection.send_requests(body=cancel_template)
        return response
        

class Confirm(CredentialUser):
    IDTransaction: Union[int, str] 
    DateTransaction: str 

    async def send_to_ws(self, connection: HttpxConnection):
        confirm_template = folder_template.get_template("sendConfirmTrans.xml")
        confirm_template = confirm_template.render(data=self)
        response = await connection.send_requests(body=confirm_template)
        return response


class GetNoConfirm(CredentialUser):
    ID_Transaction: Optional[str] = "" 
    GLN_Informador: Optional[str] = ""
    GLN_Origen: Optional[str] = ""
    GLN_Destino: Optional[str] = ""
    GTIN: Optional[str] = ""
    ID_evento: Optional[str] = ""
    Date_Trans_from: Optional[str] = ""    
    Date_Trans_to: Optional[str] = ""
    Date_Operacion_from: Optional[str] = ""
    Date_Operacion_to: Optional[str] = ""
    Date_Due_from: Optional[str] = ""
    Date_Due_to: Optional[str] = ""
    NRemito: Optional[str] = ""
    NInvoice: Optional[str] = ""
    State_Trans: Optional[str] = ""
    Lote: Optional[str] = ""
    Serie: Optional[str] = ""
    Page: Optional[str] = ""
    Offset: Optional[str] = ""

    async def send_to_ws(self, connection: HttpxConnection):
        get_no_confirm = folder_template.get_template("getNoConfirm.xml")
        get_no_confirm = get_no_confirm.render(data=self)
        response = await connection.send_requests(body=get_no_confirm)
        return response
        


class DataPaciente(BaseModel):
    id_obra_social: Optional[int]
    nro_asociado: Optional[str]
    nombres: Optional[str]
    apellido: Optional[str]
    direccion: Optional[str]
    numero:Optional[str]
    dpto: Optional[str]
    piso: Optional[str]
    provincia: Optional[str]
    localidad: Optional[str]
    n_documento: Optional[str]
    tipo_documento: Optional[str]
    n_postal: Optional[str]
    sexo: Optional[str]
    telefono: Optional[str]

    def generate_xml(self):
        etiquetas = []
        for field, value in self.model_dump().items():
            if value is not None:
                etiqueta = f"<{field}>{value}</{field}>"
                etiquetas.append(etiqueta)
        return "\n".join(etiquetas)

class IDDevolucion(IntEnum):
    NoSolicitado = 1
    SinCadenaFrio = 2
    PróximoVencer = 3
    RetiradoMercado = 4
    ErrorDocFiscal = 5
    Otros = 6

class IDEvent(IntEnum):
    pass

class SendMedicamento(CredentialUser):
    gtin: str
    gln_origen: str
    gln_destino: Optional[str] = None
    n_factura: Optional[str] = None
    n_remito: Optional[str] = None
    vencimiento: Optional[str] = None
    f_evento: str = datetime.now().strftime('%d/%m/%Y') 
    h_evento: str = datetime.now().strftime('%H:%M')  
    numero_serial: Optional[str] = None
    SerieMedFrom: Optional[str] = None
    SerieMedTo: Optional[str] = None
    id_evento:Union[int, IDEvent]
    id_programa: Optional[str] = None
    id_motivo_devolucion: Optional[Union[int, IDDevolucion]] = None
    lote: Optional[str] = None
    otro_motivo_devolucion: Optional[str] = None
    Paciente: Optional[DataPaciente] = None

    def _generate_xml(self):
        etiquetas = []
        for field, value in self.model_dump().items():
            if value is not None and field is not "Paciente":
                etiqueta = f"<{field}>{value}</{field}>"
                etiquetas.append(etiqueta)
        return "\n".join(etiquetas)

    async def send_to_ws(self, connection: HttpxConnection):
        send_Med_template = folder_template.get_template("sendMed.xml")
        data = {
            "Base": self._generate_xml(), 
            "Paciente": self.Paciente.generate_xml() if self.Paciente != None else "",
            "User":self.User, 
            "Password": self.Password
            }
        send_Med_template = send_Med_template.render(data=data)
        response = await connection.send_requests(body=send_Med_template)
        return response
