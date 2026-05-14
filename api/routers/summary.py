from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from api.database import get_db
from api.models import FinancialSummaryResponse
from typing import List

router = APIRouter(prefix="/summary", tags=["Summary"])

@router.get("/", response_model=List[FinancialSummaryResponse])
def get_all_summaries(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM financial_summary ORDER BY ano, mes"))
    return result.mappings().all()

@router.get("/usuario/{usuario_id}", response_model=List[FinancialSummaryResponse])
def get_summary_by_usuario(usuario_id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT * FROM financial_summary WHERE usuario_id = :uid ORDER BY ano, mes"),
        {"uid": usuario_id}
    )
    return result.mappings().all()

@router.get("/mes/{ano}/{mes}", response_model=List[FinancialSummaryResponse])
def get_summary_by_mes(ano: int, mes: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT * FROM financial_summary WHERE ano = :ano AND mes = :mes"),
        {"ano": ano, "mes": mes}
    )
    return result.mappings().all()