from config.database import get_database

from bson import ObjectId

db=get_database()


def insert_review(id,data):

    db.libros.update_one(

        {

            "_id":ObjectId(id)

        },

        {

            "$push":{

                "resenias":data

            }

        }

    )

    return True