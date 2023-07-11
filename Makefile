.PHONY: docs
docs: 
	typer lolpop/cli/cli.py utils docs --output docs/src/cli_reference.md --name lolpop

.PHONY: tests
tests: 
	pytest tests

all: docs tests 