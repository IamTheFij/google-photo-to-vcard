import json
import logging
import urllib.request as request
from urllib.error import HTTPError


EMAIL_TO_PHOTO_JSON_PATH = 'build/email_to_photo.json'


def write_email_photo_json(email_to_photo):
    with open(EMAIL_TO_PHOTO_JSON_PATH, 'w') as f:
        f.write(json.dumps(email_to_photo))


def read_email_photo_json():
    with open(EMAIL_TO_PHOTO_JSON_PATH, 'r') as f:
        return json.loads(f.read())


def build_photo_path(email):
    return 'build/photos/{}.jpeg'.format(email)


def download_url_to_path(url, path):
    try:
        with open(path, mode='xb') as f, request.urlopen(url) as r:
            f.write(r.read())
            return path
    except HTTPError as e:
        logging.error(e)
        return None
