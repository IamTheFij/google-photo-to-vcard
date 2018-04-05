import json
import logging
import urllib.request as request
from urllib.error import HTTPError
from hashlib import md5


EMAIL_TO_PHOTO_JSON_PATH = 'build/email_to_photo.json'


def write_email_photo_json(email_to_photo):
    with open(EMAIL_TO_PHOTO_JSON_PATH, 'w') as f:
        f.write(json.dumps(email_to_photo))


def read_email_photo_json():
    with open(EMAIL_TO_PHOTO_JSON_PATH, 'r') as f:
        return json.loads(f.read())


def build_photo_path(email):
    return 'build/photos/{}.jpeg'.format(email.lower())


def download_url_to_path(url, path):
    try:
        with request.urlopen(url) as r:
            with open(path, mode='xb') as f:
                f.write(r.read())
            return path
    except HTTPError as e:
        logging.error(e)
        return None


def generate_gravatar_url(email, size=200, default='404'):
    email_hash = md5(email.lower().encode('utf-8')).hexdigest()
    return 'https://www.gravatar.com/avatar/{}?s={}&d={}'.format(
        email_hash, str(size), default
    )
