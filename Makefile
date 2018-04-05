.PHONY: default
default: add-photos

virtualenv: virtualenv_run

virtualenv_run:
	virtualenv --python python3 virtualenv_run
	./virtualenv_run/bin/pip install -r ./requirements.txt

build/email_to_photo.json: virtualenv_run
	mkdir -p build
	./virtualenv_run/bin/python -m google_photo_to_vcard.build_photo_json

build/vdirsyncer: virtualenv_run
	./vdirsyncer-wrapper discover

build/contacts/contacts/DOWNLOADED: build/vdirsyncer
	./vdirsyncer-wrapper sync
	touch build/contacts/contacts/DOWNLOADED

.PHONY: khard-list
khard-list: build/contacts/contacts/DOWNLOADED
	./khard-wrapper list

build/photos/DONE: build/email_to_photo.json
	./virtualenv_run/bin/python -m google_photo_to_vcard.download_photos
	touch build/photos/DONE

.PHONY: add-photos
add-photos: virtualenv_run build/email_to_photo.json build/contacts/contacts/DOWNLOADED
	mkdir -p build/photos
	./virtualenv_run/bin/python -m google_photo_to_vcard.add_photo

.PHONY: clean-build
clean-build:
	rm -fr build/

.PHONY: sync-contacts
sync-contacts: build/vdirsyncer
	./vdirsyncer-wrapper sync
