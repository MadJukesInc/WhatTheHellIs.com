.PHONY: docs test

help:
	@echo "  env         create a development environment using virtualenv"
	@echo "  deps        install dependencies using pip"
	@echo "  clean       remove unwanted files like .pyc's"
	@echo "  lint        check style with flake8"
	@echo "  test        run all your tests using py.test"

env:
	sudo easy_install pip && \
	pip install virtualenv && \
	virtualenv env && \
	. env/bin/activate && \
	make deps

deps:
	@echo " You will need to install libxml2-dev(el) and libxslt-dev(el)"
	pip install -r requirements.txt
	python -m nltk.downloader punkt
	python -m textblob.download_corpora       

clean:
	python manage.py clean

lint:
	flake8 --exclude=env .

test:
	py.test tests
