from services.image_search_service import search_similar_books

resultado = search_similar_books(
    "data/imagenes/dracula_1.png"
)

print(resultado[0]["score"])

print(
    resultado[0]["book_data"]["book"]["titulo"]
)

print(
    resultado[0]["book_data"]["author"]["nombre"]
)

print(
    len(resultado[0]["book_data"]["images"])
)