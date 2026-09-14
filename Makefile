# Every target except `refresh` runs from the committed cache in data/raw/ and needs no token.
PYTHON ?= $(shell [ -x .venv/bin/python ] && echo .venv/bin/python || echo python3)

.PHONY: all pull refresh audit metrics venv

all: pull audit metrics

# Verify data/raw/ against _manifest.json (sha256 + record counts). No network.
pull:
	$(PYTHON) src/pull.py

# Re-pull every table from Airtable. The only target that uses AIRTABLE_TOKEN.
refresh:
	$(PYTHON) src/pull.py --refresh

audit: pull
	$(PYTHON) src/audit.py

metrics: pull
	$(PYTHON) src/metrics.py

venv:
	python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
