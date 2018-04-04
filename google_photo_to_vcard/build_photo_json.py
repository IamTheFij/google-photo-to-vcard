import httplib2
import json
import logging
import os
import time

from apiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from google_photo_to_vcard.util import write_email_photo_json

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/people.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/contacts.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'People API Python Quickstart'

logging.basicConfig(level=logging.DEBUG)


def safe_execute_with_backoff(request):
    """
    Executes an http request and retries rate limit errors

    Catches HttpError and, if it's a 429, sleepts for .5s and retries
    """
    attempt = 0
    sleep_time = .5

    while True:
        try:
            return request.execute()
        except HttpError as error:
            logging.info('Got HttpError')
            if error.resp.status == 429:
                sleep_for = sleep_time * (2 ** attempt)
                logging.info('Sleeping for %.3g second(s)', sleep_for)
                time.sleep(sleep_for)
                attempt += 1
            else:
                raise error


def get_all_results(api, request, key='connections'):
    logging.info('Getting first results')
    results = safe_execute_with_backoff(request)

    for result in results.get(key, []):
        yield result

    request = api.list_next(request, results)
    while request:
        logging.info('Getting next...')
        results = safe_execute_with_backoff(request)

        for result in results.get(key, []):
            yield result

        request = api.list_next(request, results)
        if not request:
            logging.info('No next page :(')


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(
        credential_dir,
        'people.googleapis.com-python-quickstart.json'
    )

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        logging.info('Storing credentials to ' + credential_path)
    return credentials


def get_primary_photo(person):
    """Accepts a person from a connections request and returns the primary photo
    if it exists."""
    for photo in person.get('photos', []):
        if photo.get('metadata', {}).get('primary'):
            return photo['url']

    return None


def main():
    """Shows basic usage of the Google People API.

    Creates a Google People API service object and outputs the name if
    available of 10 connections.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build(
        'people', 'v1', http=http,
        discoveryServiceUrl='https://people.googleapis.com/$discovery/rest'
    )

    connections = get_all_results(
        api=service.people().connections(),
        request=service.people().connections().list(
            resourceName='people/me',
            pageSize=100,
            personFields='emailAddresses,photos',
        ),
        key='connections',
    )

    all_photos = set()
    email_to_photo = {}
    count = 0

    for person in connections:
        count += 1

        primary_photo = get_primary_photo(person)
        if not primary_photo:
            continue

        emails = person.get('emailAddresses', [])
        if emails:
            all_photos.add(primary_photo)

        for email in emails:
            email_to_photo[email['value']] = primary_photo

        if count % 50 == 0:
            logging.info('Found {} photos for {} emails'.format(
                len(all_photos),
                len(email_to_photo),
            ))

    write_email_photo_json(email_to_photo)
    logging.info('All done!')
    logging.info('Found {} photos for {} emails'.format(
        len(all_photos),
        len(email_to_photo),
    ))


if __name__ == '__main__':
    main()
