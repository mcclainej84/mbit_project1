from flask import Blueprint, request, make_response
from . import controller

bp = Blueprint('pictures', __name__, url_prefix='/')

@bp.post("/pictures")
def post_picture():
    min_confidence = int(request.args.get("min_confidence", 80))

    #input check
    if not request.is_json or "data" not in request.json:
        return make_response({"description": "Debes incluir la foto en base64 como un campo llamado data en el body"}, 400)

    b64picture = request.json["data"]

    filename = controller.randomizer_name()

    controller.post_picture(b64picture,filename,min_confidence )

    return make_response({"description": "Archivo subido correctamente" }, 200)


@bp.get("/pictures")
def get_images():
    min_date = request.args.get("min_date")
    max_date = request.args.get("max_date")
    tags     = request.args.get("tags")

    data = controller.get_images(min_date,max_date,tags)

    return data

@bp.get("/picture")
def get_image():
    id = request.args.get("id")

    if not id:
        return make_response({"description": "No hay ID especificado, por favor especifique un ID"}, 400)

    data = controller.get_image(id)

    return data

@bp.get("/tags")
def get_tags():
    min_date = request.args.get("min_date")
    max_date = request.args.get("max_date")

    data = controller.get_tags(min_date,max_date)

    return data
