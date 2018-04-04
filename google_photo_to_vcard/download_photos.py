import urllib.request as request
from pathlib import Path
from urllib.error import HTTPError

from google_photo_to_vcard.util import build_photo_path
from google_photo_to_vcard.util import download_url_to_path
from google_photo_to_vcard.util import read_email_photo_json


def main():
    email_to_photo = read_email_photo_json()
    for email, photo_url in email_to_photo.items():
        print(email, photo_url)
        photo_path = Path(build_photo_path(email))
        if photo_path.exists():
            print('Photo already downloaded')
            continue
        else:
            download_url_to_path(photo_url, photo_path)


if __name__ == '__main__':
    main()
