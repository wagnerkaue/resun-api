from contextlib import asynccontextmanager
from datetime import date
from typing import Optional, cast

from fastapi import FastAPI, HTTPException, Request, Depends, Query
from google.cloud import firestore
from starlette.datastructures import State

from auth import get_firestore_client
from modelos import Campus, Fornecedor, Cardapio, TipoRefeicao, Alimento, CardapioCompleto


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state = cast(State, app.state)
    app.state.db = get_firestore_client()
    print("Aplicação iniciada")
    yield
    print("Aplicação encerrada")


app = FastAPI(lifespan=lifespan)


def get_db(request: Request) -> firestore.Client:
    db = getattr(request.app.state, "db", None)
    if not db:
        raise HTTPException(status_code=503, detail="Firestore não disponível")
    return db


async def _obter_alimentos_por_ids(db: firestore.Client, ids: list[str]) -> list[Alimento]:
    """Função auxiliar para buscar documentos de alimentos por uma lista de IDs."""
    if not ids:
        return []

    alimentos_map = {}
    refs = [db.collection("alimentos").document(id) for id in ids]

    docs = db.get_all(refs)

    for doc in docs:
        if doc.exists:
            alimento = Alimento(**doc.to_dict())
            alimentos_map[alimento.id] = alimento

    return [alimentos_map[id] for id in ids if id in alimentos_map]


@app.get(path="/cardapios", summary="Obter lista de cardápios", response_model=list[CardapioCompleto])
async def obter_cardapios(
        campus: Optional[list[Campus]] = Query(None),
        tipo_refeicao: Optional[list[TipoRefeicao]] = Query(None),
        fornecedor: Optional[list[Fornecedor]] = Query(None),

        data: Optional[date] = None,
        data_inicio: Optional[date] = None,
        data_fim: Optional[date] = None,

        limite: int = Query(
            default=10,
            gt=0,
            le=100,
            description="Número máximo de cardápios a serem retornados."
        ),

        db: firestore.Client = Depends(get_db)
):
    try:
        query = db.collection("cardapios")

        if campus:
            campus_values = [c.value for c in campus]
            query = query.where("campus", "in", campus_values)
        if tipo_refeicao:
            refeicao_values = [r.value for r in tipo_refeicao]
            query = query.where("tipo_refeicao", "in", refeicao_values)
        if fornecedor:
            fornecedor_values = [f.value for f in fornecedor]
            query = query.where("fornecedor", "in", fornecedor_values)

        if data:
            query = query.where("data", "==", data.isoformat())
        else:
            if data_inicio:
                query = query.where("data", ">=", data_inicio.isoformat())
            if data_fim:
                query = query.where("data", "<=", data_fim.isoformat())

        query = query.limit(limite)
        docs = query.stream()

        cardapios_completos = []
        for doc in docs:
            cardapio_base = Cardapio(**doc.to_dict())
            alimentos = await _obter_alimentos_por_ids(db, cardapio_base.id_alimentos)

            cardapio_dict = cardapio_base.model_dump()
            del cardapio_dict['id_alimentos']

            cardapio_completo = CardapioCompleto(**cardapio_dict, id_alimentos=alimentos)

            cardapios_completos.append(cardapio_completo)

        return cardapios_completos

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao consultar o Firestore: {e}"
        )


@app.get(path="/cardapios/{id_cardapio}", summary="Obter cardápio pelo ID", response_model=CardapioCompleto)
async def obter_cardapio_dado_id(id_cardapio: str, db: firestore.Client = Depends(get_db)):
    doc_ref = db.collection("cardapios").document(id_cardapio)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Cardápio não encontrado")

    cardapio_base = Cardapio(**doc.to_dict())
    alimentos = await _obter_alimentos_por_ids(db, cardapio_base.id_alimentos)

    cardapio_dict = cardapio_base.model_dump()
    del cardapio_dict['id_alimentos']

    return CardapioCompleto(**cardapio_dict, id_alimentos=alimentos)


@app.get(path="/alimentos", summary="Obter lista de todos os alimentos", response_model=list[Alimento])
async def obter_alimentos(db: firestore.Client = Depends(get_db)):
    docs = db.collection("alimentos").stream()
    return [Alimento(**doc.to_dict()) for doc in docs]


@app.get(path="/alimentos/{id_alimento}", summary="Obter alimento pelo ID", response_model=Alimento)
async def obter_alimento_dado_id(id_alimento: str, db: firestore.Client = Depends(get_db)):
    doc_ref = db.collection("alimentos").document(id_alimento)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Alimento não encontrado")

    return Alimento(**doc.to_dict())


@app.get(path="/campi", summary="Obter lista de todos os campi")
def obter_campi():
    return [campus.value for campus in Campus]


@app.get(path="/fornecedores", summary="Obter lista de todos fornecedores")
def obter_fornecedores():
    return [fornecedor.value for fornecedor in Fornecedor]


@app.get("/tipos-refeicao", summary="Obter lista de todos tipos de refeição")
def obter_tipos_refeicao():
    return [refeicao.value for refeicao in TipoRefeicao]