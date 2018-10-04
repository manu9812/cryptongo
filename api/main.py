import pymongo
from flask import Flask, request

app = Flask(__name__)

"""
jsonify: convierte diccionarios de python al formato json
"""

def get_db_connection(uri):
    """
    Define la conexión a la BD.
    MongoClient por defecto se conecta al localhost.
    :param uri: URI de conexión.
    :return: BD a utilizar.
    """
    client = pymongo.MongoClient(uri)
    return client.cryptongo


db_connection = get_db_connection('mongodb://localhost:27017/')


def get_documents():
    """
    Obtiene todos los documentos de la coleccion de la BD.
    :return: Una lista de los documentos según el criterio de búsqueda.
    """

    params = {}
    # request: Recibe la petición de la url y los parámetros (si tiene).
    name = request.args.get('name', '')  # Si no hay valor, será un str vacío.
    limit = int(request.args.get('limit', 0))

    if name:
        params.update({'name': name})  # Añade el valor al diccionario.

    # Se define que no se muestre los campos _id y ticker_hash.
    cursor = db_connection.tickers.find(params, {'_id': 0, 'ticker_hash': 0}).limit(limit)

    return list(cursor)


def get_rank_top20():
    """
    Obtiene los documentos que tienen un ranking menor o igual a 20.
    :return: Una lista de los documentos según el criterio de búsqueda.
    """

    params = {}
    name = request.args.get('name', '')
    limit = int(request.args.get('limit', 0))

    if name:
        params.update({'name': name})

    params.update({'rank': {'$lte': 20}})

    cursor = db_connection.tickers.find(params, {'_id': 0, 'ticker_hash': 0}).limit(limit)

    return list(cursor)


def remove_currency():
    """
    Eliminar uno o varios documentos de la coleccion según el nombre de la criptomoneda.
    :return: La cantidad de documentos eliminados.
    """

    params = {}
    name = request.args.get('name', '')

    if name:
        params.update({'name': name})
    else:
        # El método sin parámetros eliminaría todos los documentos, por lo cuál no se debe permitir.
        return False

    return db_connection.tickers.delete_many(params).deleted_count
