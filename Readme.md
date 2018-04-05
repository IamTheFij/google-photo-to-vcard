# Google Photo to VCard

A set of scripts to download profile images from Google and write them to vcards. Useful for completing the migration from Google to Nextcloud or ownCloud.

## Setup

To run, you first need to set up a few config files

### Google Credentials

To get people info from your Google account, you first need to create an application from the Google Cloud Console and then download your credentials.

1. Go to https://console.developers.google.com and create a new project
1. Add access to the Google People API (Library > Search for People > Enable)
1. Create a new set of credentials (Credentials > Create credentials > OAuth client ID > other (Give it a name) > Create)
1. Click the download icon next to the new credentials and save to this project directory as `client_secret.json`


### Vdirsyncer Config

This is the config that will allow you to sync to and from your remote VCard directory. The following instructions are for Nextcloud, but you can refer to the [official documentation](https://vdirsyncer.pimutils.org/en/stable/tutorial.html) for more instructions.

Edit ./vdirsyncer.conf.example adding your server url, username, and password in the `[storage my_contacts_remote]` section.

## Running

Once your configuration is set up, you should be able to download and add photos to all your contacts by executing:

```
make add-photos
```

It's then worth taking a look and making sure that the results are as you expected. When you're happy with them, you can push the contacts back up to your remote server by running:

```
make sync-contacts
```
