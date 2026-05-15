from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from api.database import get_db
from api.models import FinancialSummaryResponse
from api.security import verify_api_key
from typing import List

router = APIRouter(prefix="/summary", tags=["Summary"])

@router.get("/", response_model=List[FinancialSummaryResponse])
def get_all_summaries(
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
    page: int = 1,
    limit: int = 20
):
    offset = (page - 1) * limit
    result = db.execute(
        text("SELECT * FROM financial_summary ORDER BY ano, mes LIMIT :limit OFFSET :offset"),
        {"limit": limit, "offset": offset}
    )
    return result.mappings().all()

@router.get("/usuario/{usuario_id}", response_model=List[FinancialSummaryResponse])
def get_summary_by_usuario(usuario_id: int, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    result = db.execute(
        text("SELECT * FROM financial_summary WHERE usuario_id = :uid ORDER BY ano, mes"),
        {"uid": usuario_id}
    )
    return result.mappings().all()

@router.get("/mes/{ano}/{mes}", response_model=List[FinancialSummaryResponse])
def get_summary_by_mes(ano: int, mes: int, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    result = db.execute(
        text("SELECT * FROM financial_summary WHERE ano = :ano AND mes = :mes"),
        {"ano": ano, "mes": mes}
    )
    return result.mappings().all()

@router.get("/categorias/{usuario_id}")
def get_gastos_por_categoria(usuario_id: int, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    result = db.execute(
        text("""
            SELECT
                cat.nome AS categoria,
                t.tipo,
                SUM(t.valor) AS total
            FROM transacoes t
            JOIN contas c ON t.conta_id = c.id
            JOIN categorias cat ON t.categoria_id = cat.id
            WHERE c.usuario_id = :uid
            GROUP BY cat.nome, t.tipo
            ORDER BY total DESC
        """),
        {"uid": usuario_id}
    )
    return result.mappings().all()

@router.get("/totais")
def get_totais_gerais(db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    result = db.execute(text("""
        SELECT
            COUNT(DISTINCT usuario_id) AS total_usuarios,
            ROUND(AVG(receita), 2) AS media_receita,
            ROUND(AVG(despesa), 2) AS media_despesa,
            ROUND(AVG(saldo_liquido), 2) AS media_saldo,
            ROUND(SUM(receita), 2) AS total_receita,
            ROUND(SUM(despesa), 2) AS total_despesa,
            ROUND(SUM(saldo_liquido), 2) AS total_saldo
        FROM financial_summary
    """))
    return result.mappings().one()