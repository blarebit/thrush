SRC_DIR ?= thrush

.PHONY: new-component
new-component:
	cd $(SRC_DIR) && python manage.py startapp $(app)
	find $(SRC_DIR)/ -iname "admin.py" -delete

.PHONY: dev
dev:
	cd $(SRC_DIR) && python3 manage.py runserver 8000

.PHONY: run
run:
	cd $(SRC_DIR) && ./init.sh

.PHONY: lint
lint:
	flake8 $(SRC_DIR)/
	isort -c $(SRC_DIR)/
	pylint $(SRC_DIR)/
	black --check $(SRC_DIR)/

.PHONY: test
test:
	cd $(SRC_DIR) && python manage.py test

.PHONY: package
package:
	python -m build

.PHONY: image
image:
	docker build -t thrush -f deploy/docker/Dockerfile .

.PHONY: docker-compose
docker-compose:
	docker-compose -f deploy/docker/docker-compose.yaml up

