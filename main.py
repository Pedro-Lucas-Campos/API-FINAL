from fastapi import FastAPI
from pydantic import BaseModel
import datetime
from zoneinfo import ZoneInfo

app = FastAPI(
    title="API de Registro de Veículos",
    description="Recebe dados de VIN e Localização e os salva em um arquivo CSV central."
)
database = []

class Record(BaseModel):
    VIN: str
    Localização: str
    Tipo : str

@app.post("/add_record", status_code=201)
def registrar_dado(dado: Record):
    fuso_horario = ZoneInfo("America/Sao_Paulo")
    dado_dict = dado.model_dump()
    timestamplocal = datetime.datetime.now(fuso_horario)
    dado_dict["timestamp"] = datetime.datetime.now().isoformat()
    database.append(dado_dict)
    return {"mensagem": "Dado recebido com sucesso", "dados": dado_dict}

@app.get("/dados")
def obter_dados():
    return database