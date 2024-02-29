from datetime import datetime
from enum import IntEnum
from pydantic import BaseModel, Field
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
    ID_Transaction: Optional[str] = Field(default="") 
    GLN_Informador: Optional[str] = Field(default="")
    GLN_Origen: Optional[str] = Field(default="")
    GLN_Destino: Optional[str] = Field(default="")
    GTIN: Optional[str] = Field(default="")
    ID_evento: Optional[str] = Field(default="")
    Date_Trans_from: Optional[str] = Field(default="")    
    Date_Trans_to: Optional[str] = Field(default="")
    Date_Operacion_from: Optional[str] = Field(default="")
    Date_Operacion_to: Optional[str] = Field(default="")
    Date_Due_from: Optional[str] = Field(default="")
    Date_Due_to: Optional[str] = Field(default="")
    NRemito: Optional[str] = Field(default="")
    NInvoice: Optional[str] = Field(default="")
    State_Trans: Optional[str] = Field(default="")
    Lote: Optional[str] = Field(default="")
    Serie: Optional[str] = Field(default="")
    Page: Optional[str] = Field(default="")
    Offset: Optional[str] = Field(default="")

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
    gtin: str = Field(max_length=14)
    gln_origen: str = Field(max_length=13)
    gln_destino: Optional[str] = Field(default=None, max_length=13)
    n_factura: Optional[str] = Field(default=None, max_length=20)
    n_remito: Optional[str] = Field(default=None, max_length=20)
    vencimiento: Optional[str] = Field(default=None, max_length=10)
    f_evento: str = Field(default=datetime.now().strftime('%d/%m/%Y')) 
    h_evento: str = Field(default=datetime.now().strftime('%H:%M'))  
    numero_serial: Optional[str] = Field(default=None, max_length=20)
    SerieMedFrom: Optional[str] = None
    SerieMedTo: Optional[str] = None
    id_evento:Union[int, IDEvent]
    id_programa: Optional[str] = None
    id_motivo_devolucion: Optional[Union[int, IDDevolucion]] = None
    lote: Optional[str] = Field(default=None, max_length=20)
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

class GetCatalogoByGLN(CredentialUser):
    GLN: Optional[str] = Field(default="", max_length=13)
    CUIT: Optional[str] = Field(default="", max_length=11)
    Razon_social: Optional[str] = Field(default="", max_length=150)
    Id_prov: Optional[str] = Field(default="")
    Page: int = Field(default=1)
    Offset: int = Field(default=10) 

    async def send_to_ws(self, connection: HttpxConnection):
        get_catalogo = folder_template.get_template("getCatalogoElectronicoByGLN.xml")
        get_catalogo = get_catalogo.render(data=self)
        response = await connection.send_requests(body=get_catalogo)
        return response