from repositories.autores_repository import (
    get_all_authors,
    get_author,
    get_complete_author
)


def obtener_autores():

    return get_all_authors()


def obtener_autor(id):

    return get_author(id)

def obtener_autor_completo(id):

    return get_complete_author(id)