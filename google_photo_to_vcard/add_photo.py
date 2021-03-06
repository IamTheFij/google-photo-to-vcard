import logging
from pathlib import Path

import vobject

from google_photo_to_vcard.util import build_photo_path
from google_photo_to_vcard.util import download_url_to_path
from google_photo_to_vcard.util import generate_gravatar_url
from google_photo_to_vcard.util import read_email_photo_json


logging.basicConfig(level=logging.DEBUG)


def open_card(card_path):
    with open(card_path, mode='r') as f:
        return vobject.readOne(f.read())


def maybe_add_photo(card, photo_path):
    if hasattr(card, 'photo'):
        logging.info('%s has photo', card.fn.value)
        return False
    photo = card.add('photo')
    photo.params = {
        'ENCODING': ['b'],
        'TYPE': ['JPEG'],
    }

    with open(photo_path, mode='rb') as f:
        photo.value = f.read()

    return True


def write_card_to_path(card, card_path):
    with open(card_path, mode='w') as f:
        f.write(card.serialize())


def generate_card_paths():
    base_path = 'build/contacts/contacts'
    for card_path in Path(base_path).glob('*.vcf'):
        if card_path.is_file():
            yield str(card_path)


def generate_cards():
    for card_path in generate_card_paths():
        yield open_card(card_path), card_path


def main():
    email_to_photo = read_email_photo_json()
    for card, card_path in generate_cards():
        if hasattr(card, 'photo'):
            logging.info('%s has photo', card.fn.value)
            continue
        for email_elem in card.contents.get('email', []):
            email = email_elem.value
            photo_path = Path(build_photo_path(email))
            if not photo_path.exists():
                if email in email_to_photo:
                    logging.debug('Downloading google photo for %s', card.fn.value)
                    download_url_to_path(email_to_photo[email], photo_path)
                else:
                    logging.debug('Downloading Gravatar photo for %s', card.fn.value)
                    gravatar_url = generate_gravatar_url(email)
                    download_url_to_path(gravatar_url, photo_path)
            if photo_path.exists():
                if maybe_add_photo(card, photo_path):
                    write_card_to_path(card, card_path)
                    logging.info('Added photo to %s', card.fn.value)
                    break


if __name__ == '__main__':
    main()
