"""
image_embedding_service.py

Genera embeddings para imágenes usando CLIP.
El modelo se carga una sola vez al iniciar la aplicación.
"""

from sentence_transformers import SentenceTransformer
from PIL import Image

_model = SentenceTransformer("clip-ViT-B-32")


def get_image_embedding(image_path: str) -> list[float]:
    """
    Recibe la ruta de una imagen y devuelve su embedding.
    """

    image = Image.open(image_path).convert("RGB")

    embedding = _model.encode(
        image,
        normalize_embeddings=True
    )

    return embedding.tolist()