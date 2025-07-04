from fastapi import FastAPI
from pydantic import BaseModel
import datetime
from datetime import timezone 
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
    timestamp_utc = datetime.datetime.now(timezone.utc)

    fuso_horario_sp = ZoneInfo("America/Sao_Paulo")
    timestamp_sp = timestamp_utc.astimezone(fuso_horario_sp)

    dado_dict = dado.model_dump()

    dado_dict["timestamp_utc"] = timestamp_utc.isoformat()
    dado_dict["timestamp_sao_paulo"] = timestamp_sp.isoformat()
    
    database.append(dado_dict)
    
    return {"mensagem": "Dado recebido com sucesso", "dados": dado_dict}

@app.get("/dados")
def obter_dados():
    return database
