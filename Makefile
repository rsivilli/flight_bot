.PHONY: test
test: export PYTHONPATH=.
test:
	pytest


.PHONY: updatestore
updatestore:
	python ./scripts/grabmac.py



.PHONY: createenv
createenv:
	conda env create -f ./environment.yml
	conda activate flight_bot
	pip install -e .

.PHONY: updatenv
updatenv:
	conda env update --file environment.yml  --prune



