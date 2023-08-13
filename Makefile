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

.phony: example_medical_bills
example_medical_bills: 
	kaggle datasets download mirichoi0218/insurance 
	unzip -o insurance.zip -d examples/quickstart/regression/medical_bills
	#split into test/train files
	split -l 1000 examples/quickstart/regression/medical_bills/insurance.csv csv_
	echo $$(head -1 csv_aa) | cat - csv_ab > tmp
	awk 'BEGIN{FS=OFS=","}{NF--;print}' tmp > examples/quickstart/regression/medical_bills/test.csv 
	mv csv_aa examples/quickstart/regression/medical_bills/train.csv
	rm csv_ab tmp insurance.zip examples/quickstart/regression/medical_bills/insurance.csv

examples: example_titanic example_medical_bills
	
