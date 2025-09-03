from contextlib import asynccontextmanager
from datetime import date
from typing import Optional, cast

from fastapi import FastAPI, HTTPException, Request, Depends
from google.cloud import firestore
from starlette.datastructures import State

from auth import get_firestore_client
from modelos import Campus, Fornecedor, Cardapio, TipoRefeicao


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


@app.get(path="/cardapios", summary="Obter lista de cardápios", response_model=list[Cardapio])
async def obter_cardapios(
        campus: Optional[Campus] = None,
        data: Optional[date] = None,
        tipo_refeicao: Optional[TipoRefeicao] = None,
        data_inicio: Optional[date] = None,
        data_fim: Optional[date] = None,
        db: firestore.Client = Depends(get_db)
):
    query = db.collection("cardapios")

    if campus:
        query = query.where("campus", "==", campus.value)

    if tipo_refeicao:
        query = query.where("refeicao", "==", tipo_refeicao.value)

    if data:
        query = query.where("data", "==", data.isoformat())
    else:
        if data_inicio:
            query = query.where("data", ">=", data_inicio.isoformat())
        if data_fim:
            query = query.where("data", "<=", data_fim.isoformat())

    try:
        docs = query.stream()

        cardapios_validos = []
        for doc in docs:
            try:
                cardapios_validos.append(Cardapio(**doc.to_dict()))
            except Exception as e:
                print(f"Erro ao converter documento {doc.id}: {e}")

        return cardapios_validos

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao consultar o Firestore: {e}"
        )


@app.get(path="/cardapios/{id_cardapio}", summary="Obter cardápio pelo ID", response_model=Cardapio)
async def obter_cardapio_dado_id(id_cardapio: str, db: firestore.Client = Depends(get_db)):
    doc_ref = db.collection("cardapios").document(id_cardapio)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Cardápio não encontrado")

    return Cardapio(**doc.to_dict())


@app.get(path="/campi", summary="Obter lista de todos os campi")
def obter_campi():
    return [campus.value for campus in Campus]


@app.get(path="/fornecedores", summary="Obter lista de todos fornecedores")
def obter_fornecedores():
    return [fornecedor.value for fornecedor in Fornecedor]


@app.get("/tipos-refeicao", summary="Obter lista de todos tipos de refeição")
def obter_tipos_refeicao():
    return [refeicao.value for refeicao in TipoRefeicao]
