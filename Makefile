.PHONY: dev
dev:
	cd aap && python manage.py collectstatic && python3 manage.py runserver 8000

.PHONY: run
run:
	cd aap && python manage.py collectstatic
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

.PHONY: image
image:
	docker build -t aap -f deploy/docker/Dockerfile .
