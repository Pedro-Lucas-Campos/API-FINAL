from fastapi import FastAPI
from pydantic import BaseModel
import datetime

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
    dado_dict = dado.model_dump()
    dado_dict["timestamp"] = datetime.datetime.now().isoformat()
    database.append(dado_dict)
    return {"mensagem": "Dado recebido com sucesso", "dados": dado_dict}

@app.get("/dados")
def obter_dados():
    return database