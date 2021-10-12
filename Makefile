.PHONY: dev
dev:
	cd aap && python3 manage.py runserver 8000

.PHONY: run
run:
	PYTHONPATH=aap gunicorn aap.wsgi

.PHONY: lint
lint:
	flake8 aap/
	#isort -c aap/
	#pylint aap/
	black --check aap/

.PHONY: test
test:
	python manage.py test

.PHONY: package
package:
	python -m build