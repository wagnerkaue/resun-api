from auth import get_firestore_client
from scraping.extracao import extrair_cardapios_api


def fazer_upload_cardapios():
    print("Iniciando extração dos cardápios...")
    lista_cardapios = extrair_cardapios_api()

    if not lista_cardapios:
        print("Nenhum cardápio foi extraído.")
        return

    db = get_firestore_client()
    collection_ref = db.collection("cardapios")

    print(f"Iniciando upload de {len(lista_cardapios)} cardápios para o Firestore...")

    for cardapio in lista_cardapios:
        cardapio_dict = cardapio.model_dump()
        doc_id = cardapio.id
        collection_ref.document(doc_id).set(cardapio_dict)
        print(f" -> Documento '{doc_id}' salvo com sucesso.")

    print("\nUpload concluído!")


if __name__ == "__main__":
    fazer_upload_cardapios()
