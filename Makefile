.PHONY: default
default: run

.PHONY: run
run: email_to_photo.json

virtualenv: virtualenv_run

virtualenv_run:
	virtualenv --python python3 virtualenv_run
	./virtualenv_run/bin/pip install -r ./requirements.txt

build/email_to_photo.json: virtualenv_run
	mkdir -p build
	./virtualenv_run/bin/python -m google_photo_to_vcard.build_photo_json

build/vdirsyncer: virtualenv_run
	./vdirsyncer-wrapper discover

build/vdirsyncer/status/my_contacts/contacts.items: build/vdirsyncer
	./vdirsyncer-wrapper sync

.PHONY: sync-contacts
sync-contacts: build/vdirsyncer/status/my_contacts/contacts.items

.PHONY: khard-list
khard-list: build/vdirsyncer/status/my_contacts/contacts.items
	./khard-wrapper list

build/photos/DONE: build/email_to_photo.json
	./virtualenv_run/bin/python -m google_photo_to_vcard.download_photos
	touch build/photos/DONE

.PHONY: add-photos
add-photos: virtualenv_run build/email_to_photo.json build/vdirsyncer/status/my_contacts/contacts.items
	mkdir -p build/photos
	./virtualenv_run/bin/python -m google_photo_to_vcard.add_photo
