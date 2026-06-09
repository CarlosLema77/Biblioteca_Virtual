from repositories.libros_repository import (
    actualizar_libro,
    eliminar_libro,
    get_all_books,
    get_book_by_id,
    get_books_by_author,
    get_books_by_genre,
    get_featured_books,
    get_complete_book,
    insertar_libro
)


def obtener_libros():

    return get_all_books()


def obtener_libro(id):

    return get_book_by_id(id)


def obtener_libros_autor(id):

    return get_books_by_author(id)


def obtener_libros_genero(genero):

    return get_books_by_genre(genero)


def obtener_destacados():

    return get_featured_books()

def obtener_libro_completo(id):

    return get_complete_book(id)

def crear_libro(data):

    return insertar_libro(data)


def editar_libro(id,data):

    return actualizar_libro(id,data)


def borrar_libro(id):

    return eliminar_libro(id)