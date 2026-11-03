.PHONY: dev test-dev

dev:
	python3 scripts/dev.py

test-dev:
	python3 -m unittest discover -s scripts -p 'test_dev.py'
