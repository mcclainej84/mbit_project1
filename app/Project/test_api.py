import json



def get_api_credentials():
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)

    return credentials["imagekit"],credentials["imagga"]

imagekit, imagga = get_api_credentials()


print(imagekit["public_key"])
