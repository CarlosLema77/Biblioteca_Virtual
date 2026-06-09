from bson import ObjectId
from datetime import datetime


def serialize_doc(doc):
    """Convierte documentos MongoDB a datos serializables."""
    if doc is None:
        return None

    if isinstance(doc, list):
        return [serialize_doc(d) for d in doc]

    if isinstance(doc, dict):
        return {k: serialize_doc(v) for k, v in doc.items()}

    if isinstance(doc, ObjectId):
        return str(doc)

    if isinstance(doc, datetime):
        return doc.isoformat()

    return doc


def parse_mongo_document(doc):
    """
    Compatibilidad con el código existente.
    """
    return serialize_doc(doc)