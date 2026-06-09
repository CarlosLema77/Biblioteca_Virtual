import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from config.database import get_database
from services.image_embedding_service import get_image_embedding


db = get_database()


def generate_embeddings():

    imagenes = list(db.imagenes.find({}))

    print(f"\n📸 Imágenes encontradas: {len(imagenes)}\n")

    for i, imagen in enumerate(imagenes, start=1):

        path = imagen.get("path_local")

        if not path:
            print(f"[{i}] Sin path_local")
            continue

        if not os.path.exists(path):
            print(f"[{i}] No existe: {path}")
            continue

        try:

            embedding = get_image_embedding(path)

            db.imagenes.update_one(
                {"_id": imagen["_id"]},
                {
                    "$set": {
                        "embedding_visual": embedding,
                        "modelo_vision": "clip-ViT-B-32"
                    }
                }
            )

            print(
                f"[{i}/{len(imagenes)}] "
                f"✓ {os.path.basename(path)}"
            )

        except Exception as e:

            print(
                f"[{i}/{len(imagenes)}] "
                f"✗ Error: {e}"
            )


if __name__ == "__main__":
    generate_embeddings()