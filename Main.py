from core.deps import get_api_keys_from_header
from fastapi import Depends, FastAPI, Header
from enum import Enum
from Robot import (
    Muelle_cartagena,
    Muelle_barranquilla,
    Muelle_buenaventura,
    Muelle_tolu,
    Muelle_aguadulce,
    Muelle_Portuaria,
    Consulta_Aguadulce_2
)

app = FastAPI(title="Muelle")

# Enumeración para elegir el muelle
class TipoConsultaEnum(str, Enum):
    CARTAGENA = "Cartagena"
    BARRANQUILLA = "Barranquilla"
    BUENABENTURA = "Buenaventura"
    TOLU = "Tolu"
    AGUADULCE = "AguaDulce_compas"
    PORTUARIA = "Portuaria"
    AGUADULCE_2 = "AguaDulce_Industrial"

@app.post("/Muelle")
def consultar_Muelles(
    tipo_consulta: TipoConsultaEnum,
    authorization: bool = Depends(get_api_keys_from_header), api_key_header: str = Header(default=None, alias="X-Api-Key")
):
    try:
        if tipo_consulta == TipoConsultaEnum.CARTAGENA:
            return Muelle_cartagena()
        elif tipo_consulta == TipoConsultaEnum.BARRANQUILLA:
            return Muelle_barranquilla()
        elif tipo_consulta == TipoConsultaEnum.BUENABENTURA:
            return Muelle_buenaventura()
        elif tipo_consulta == TipoConsultaEnum.TOLU:
            return Muelle_tolu()
        elif tipo_consulta == TipoConsultaEnum.AGUADULCE:
            return Muelle_aguadulce()
        elif tipo_consulta == TipoConsultaEnum.PORTUARIA:
            return Muelle_Portuaria()
        elif tipo_consulta == TipoConsultaEnum.AGUADULCE_2:
            return Consulta_Aguadulce_2()
        else:
            return {"error": "Tipo de consulta no válida"}
    except Exception as e:
        return {"error de la consulta": str(e)}
