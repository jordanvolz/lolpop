.PHONY: docs
docs: 
	typer lolpop/cli/cli.py utils docs --output docs/src/cli_reference.md --name lolpop

.PHONY: tests
tests: 
	pytest tests

all: docs tests 

.PHONY: example_titanic
example_titanic: 
	kaggle competitions download -c titanic
	unzip -o titanic.zip -d examples/quickstart/classification/titanic
	rm titanic.zip 

examples: example_titanic
	