SKIP_DATA?=false

.PHONY: docs
docs: 
	typer lolpop/cli/cli.py utils docs --output docs/src/cli_reference.md --name lolpop

.PHONY: example_titanic
example_titanic: 
	if ! [ ${SKIP_DATA} = true ]; then \
		kaggle competitions download -c titanic ;\
		unzip -o titanic.zip -d examples/quickstart/classification/titanic ;\
	fi 
	mkdir -p examples/quickstart/classification/titanic/mlruns/.trash
	if ! [ ${SKIP_DATA} = true ]; then \
		rm titanic.zip ;\
	fi
	echo "Data for Titanic Example set up successfully!"

.phony: example_medical_bills
example_medical_bills: 
	if ! [ ${SKIP_DATA} = true ]; then \
		kaggle datasets download mirichoi0218/insurance ;\
		unzip -o insurance.zip -d examples/quickstart/regression/medical_bills ;\
		split -l 1000 examples/quickstart/regression/medical_bills/insurance.csv csv_ ;\
		echo $$(head -1 csv_aa) | cat - csv_ab > tmp ;\
		awk 'BEGIN{FS=OFS=","}{NF--;print}' tmp > examples/quickstart/regression/medical_bills/test.csv ;\
		mv csv_aa examples/quickstart/regression/medical_bills/train.csv ;\
	fi 
	mkdir -p examples/quickstart/regression/medical_bills/mlruns/.trash
	if ! [ ${SKIP_DATA} = true ]; then \
		rm csv_ab tmp insurance.zip examples/quickstart/regression/medical_bills/insurance.csv ;\
	fi
	echo "Data for Medical Bills Example set up successfully!"

.phony: example_sales_forecasting
example_sales_forecasting: 
	if ! [ ${SKIP_DATA} = true ]; then \
		kaggle datasets download podsyp/time-series-starter-dataset ;\
		unzip -o time-series-starter-dataset.zip -d examples/quickstart/timeseries/sales_forecasting ;\
		split -l 65 examples/quickstart/timeseries/sales_forecasting/Month_Value_1.csv csv_ ;\
		echo $$(head -1 csv_aa) | cat - csv_ab > examples/quickstart/timeseries/sales_forecasting/test.csv ;\
		mv csv_aa examples/quickstart/timeseries/sales_forecasting/train.csv ;\
	fi 
	mkdir -p examples/quickstart/timeseries/sales_forecasting/mlruns/.trash
	if ! [ ${SKIP_DATA} = true ]; then \
		rm time-series-starter-dataset.zip csv_ab examples/quickstart/timeseries/sales_forecasting/Month_Value_1.csv ;\
	fi 
	echo "Data for Sales Forecasting Example set up successfully!"

.phony: example_petfinder
example_petfinder: 
	if ! [ ${SKIP_DATA} = true ]; then \
		kaggle competitions download -c petfinder-adoption-prediction ;\
		unzip -j -o petfinder-adoption-prediction.zip train/train.csv test/test.csv -d examples/classification/petfinder/data ;\
	fi 
	mkdir -p examples/classification/petfinder/mlruns/.trash
	mkdir -p examples/classification/petfinder/dvc
	mkdir -p /tmp/artifacts
	cd examples/classification/petfinder && dvc init --subdir --force && dvc remote add -d local /tmp/artifacts 
	if ! [ ${SKIP_DATA} = true ]; then \
		rm petfinder-adoption-prediction.zip ;\
	fi
	echo "Data for Petfinder Adoption Example set up successfully!"

.phony: example_crabs
example_crab_age: 
	if ! [ ${SKIP_DATA} = true ]; then \
		kaggle competitions download -c playground-series-s3e16 ;\
		unzip -j -o playground-series-s3e16.zip train.csv test.csv -d examples/regression/crab_age/data ;\
	fi
	mkdir -p examples/regression/crab_age/mlruns/.trash
	mkdir -p examples/regression/crab_age/dvc
	mkdir -p /tmp/artifacts
	cd examples/regression/crab_age && dvc init --subdir --force && dvc remote add -d local /tmp/artifacts 
	mkdir -p examples/regression/crab_age/duckdb
	cd examples/regression/crab_age && python3 setup_duckdb.py
	if ! [ ${SKIP_DATA} = true ]; then \
		rm playground-series-s3e16.zip ;\
	fi
	echo "Data for Crab Age Example set up successfully!"

.phony: example_grocery_sales
example_grocery_sales: 
	if ! [ ${SKIP_DATA} = true ]; then \
		kaggle competitions download -c store-sales-time-series-forecasting ;\
		unzip -j -o store-sales-time-series-forecasting.zip train.csv test.csv holidays_events.csv -d examples/time_series/grocery_sales/data ;\
	fi 
	mkdir -p examples/time_series/grocery_sales/mlruns/.trash
	mkdir -p examples/time_series/grocery_sales/dvc
	mkdir -p /tmp/artifacts
	cd examples/time_series/grocery_sales && dvc init --subdir --force && dvc remote add -d local /tmp/artifacts 
	mkdir -p examples/time_series/grocery_sales/duckdb
	cd examples/time_series/grocery_sales && python3 setup_duckdb.py
	if ! [ ${SKIP_DATA} = true ]; then \
		rm store-sales-time-series-forecasting.zip ;\
	fi
	echo "Data for Grocery Sales Forecasting set up successfully!"

examples: example_titanic example_medical_bills example_sales_forecasting example_petfinder example_crab_age example_grocery_sales
	


.PHONY: clean_example_petfinder
clean_example_petfinder: 
	rm -rf examples/classification/petfinder/.dvc examples/classification/petfinder/dvc examples/classification/petfinder/mlruns examples/classification/petfinder/.dvcignore examples/classification/petfinder/.metaflow

.PHONY: clean_example_crab_age
clean_example_crab_age: 
	rm -rf examples/regression/crab_age/.dvc examples/regression/crab_age/dvc examples/regression/crab_age/mlruns examples/regression/crab_age/.dvcignore examples/regression/crab_age/.metaflow

.PHONY: clean_example_grocery_sales
clean_example_grocery_sales: 
	rm -rf examples/time_series/grocery_sales/.dvc examples/time_series/grocery_sales/dvc examples/time_series/grocery_sales/mlruns examples/time_series/grocery_sales/.dvcignore examples/time_series/grocery_sales/.metaflow

.PHONY: clean_example_quickstart
clean_example_quickstart: 
	rm -rf examples/quickstart/classification/titanic/mlruns examples/quickstart/regression/medical_bills/mlruns examples/quickstart/timeseries/sales_forecasting/mlruns


.PHONY: clean_examples
clean_examples: 
		rm -rf examples/classification/petfinder/.dvc examples/classification/petfinder/dvc examples/classification/petfinder/mlruns examples/classification/petfinder/.dvcignore examples/classification/petfinder/.metaflow
		rm -rf examples/regression/crab_age/.dvc examples/regression/crab_age/dvc examples/regression/crab_age/mlruns examples/regression/crab_age/.dvcignore examples/regression/crab_age/.metaflow
		rm -rf examples/time_series/grocery_sales/.dvc examples/time_series/grocery_sales/dvc examples/time_series/grocery_sales/mlruns examples/time_series/grocery_sales/.dvcignore examples/time_series/grocery_sales/.metaflow
		rm -rf examples/quickstart/classification/titanic/mlruns examples/quickstart/regression/medical_bills/mlruns examples/quickstart/timeseries/sales_forecasting/mlruns
		echo "Finished cleaning examples!"

.PHONY: tests
tests: examples
	pytest tests

all: docs examples tests 