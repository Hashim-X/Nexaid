import firebase_admin
from firebase_admin import firestore

def _get_db():
    return firestore.client()

def add_document(collection_name: str, data: dict) -> str:
    db = _get_db()
    # Adds document to Firestore collection
    # Returns the new document ID
    doc_ref = db.collection(collection_name).document()
    doc_ref.set(data)
    return doc_ref.id

def get_documents(collection_name: str, filters: list = None) -> list:
    db = _get_db()
    # Gets all documents from collection
    # filters is optional list of tuples: [("field", "==", "value")]
    # Returns list of dicts with "id" field included
    docs_ref = db.collection(collection_name)
    if filters:
        for f in filters:
            docs_ref = docs_ref.where(f[0], f[1], f[2])
    
    docs = docs_ref.stream()
    result = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data['id'] = doc.id
        result.append(doc_data)
    return result

def update_document(collection_name: str, doc_id: str, data: dict) -> None:
    db = _get_db()
    # Updates existing document by ID
    doc_ref = db.collection(collection_name).document(doc_id)
    doc_ref.update(data)
