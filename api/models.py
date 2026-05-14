from pydantic import BaseModel

class FinancialSummaryResponse(BaseModel):
    id: int
    usuario_id: int
    ano: int
    mes: int
    receita: float
    despesa: float
    saldo_liquido: float

    class Config:
        from_attributes = True