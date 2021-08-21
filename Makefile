.PHONY: checks format

checks:
	@poetry run black --check yawl tests
	@poetry run mypy yawl tests
	@poetry run flake8 .
	@poetry run pytest -n 4
	@poetry run poetry check
	@poetry run safety check --full-report
format:
	@poetry run black .