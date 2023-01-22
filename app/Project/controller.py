from . import models
from imagekitio import ImageKit
import base64
import requests
import random
import string
import os.path
import json

FORMAT = '.jpg'


"""
POST SECTION
Code and utilities for POST methods
"""
def get_api_credentials():
    with open('./project/credentials.json', 'r') as f:
        credentials = json.load(f)

    return credentials["imagekit"],credentials["imagga"]

def randomizer_name():
    #choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(6))+FORMAT

    #return a 6 letters random name
    return result_str

def get_tags_api(image_url,min_confidence,imagga_credentials):
    api_key = imagga_credentials['api_key']
    api_secret = imagga_credentials['api_secret']

    print('getting response')
    response = requests.get(f"https://api.imagga.com/v2/tags?image_url={image_url}", auth=(api_key, api_secret))

    tags = [
        (t["tag"]["en"],int(t["confidence"]) )
        for t in response.json()["result"]["tags"]
        if t["confidence"] > min_confidence
    ]

    return tags


def get_image_tags(filename,min_confidence):
    imagekit_credentials, imagga_credentials = get_api_credentials()

    imagekit = ImageKit(
        public_key=imagekit_credentials['public_key'],
        private_key=imagekit_credentials['private_key'],
        url_endpoint = imagekit_credentials['url_endpoint']
    )

    with open(f"/home/app/project/pictures_server/{filename}", mode="rb") as img:
        imgstr = base64.b64encode(img.read())

    # upload an image
    upload_info = imagekit.upload(file=imgstr, file_name=filename)

    print('upload_info.file_path:' + str(upload_info.file_path))

    print('min_confidence:' + str(min_confidence))

    # Get the tags
    tags = get_tags_api(imagekit_credentials['url_endpoint']+upload_info.file_path,min_confidence,imagga_credentials)

    # delete an image
    delete = imagekit.delete_file(file_id=upload_info.file_id)

    return tags

def save_picture(b64image,filename):
    save_path= f"/home/app/project/pictures_server/{filename}"

    img = base64.b64decode(b64image)
    with open(save_path, 'wb') as f:
        f.write(img)

    #get the size after storing the file
    size = os.path.getsize(save_path)
    return size

def post_picture(b64image,filename,min_confidence):
    #Save picture into server destination
    filesize = save_picture(b64image, filename)
    #Upload the file and obtain the tags
    tags = get_image_tags(filename,min_confidence)
    #insert file information in the DB
    models.insert_picture_and_tags(filename,filesize,tags)

"""
GET SECTION
Code and utilities for GET methods
"""
def get_b64_img(filename):
    path = f"/home/app/project/pictures_server/{filename}"
    with open(path, "rb") as f:
        bstr = f.read()
    b64str = (
        # pasamos un texto binario y nos devuelve otro texto binario, pero con un conjunto de caracteres restringido
        base64.b64encode(bstr)
        # pasamos el texto binario a texto plano, decodificando en UTF-8 (por defecto)
        .decode()
    )
    return b64str

def get_images(min_date,max_date,tags):
    data = models.get_images(min_date,max_date,tags)
    return data

def get_image(id):
    picture,tags,filename = models.get_image(id)
    del picture[0]['filename']
    picture[0]['data'] = get_b64_img(filename)
    picture[0]['tags'] = tags

    return picture

def get_tags(min_date,max_date):
    data = models.get_tags(min_date,max_date)
    return data