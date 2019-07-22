install:
	pip install -r requirements.txt
	python setup.py install

test:
	coverage run --source=ebook_homebrew -m pytest --junit-xml=test_results.xml

doc:
	cd doc_src && \
	  python make_docs.py

test-it:
	pip install -r requirements-test.txt
	coverage run --source=ebook_homebrew -m pytest --it --junit-xml=test_results.xml

test-report:
	coverage report -m
	coverage html

pypi-upload-test:
	twine upload --repository testpypi dist/*

pypi-upload:
	twine upload --repository pypi dist/*

docker-build:
	docker build -t ebook-homebrew docker

docker-run:
	docker run --rm --name ebook-homebrew -e PORT=8082 -p 8082:8082 ebook-homebrew

docker-stop:
	docker stop ebook-homebrew

.PHONY: all
