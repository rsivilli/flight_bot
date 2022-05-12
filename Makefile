.PHONY: test
test: export PYTHONPATH=.
test:
	pytest


.PHONY: updatestore
updatestore:
	python ./scripts/grabmac.py
