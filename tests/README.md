# A note on python versions

The example_tests are generally expected to be validated with whatever python versions are intended to be supported. The general procedure to run a test should be: 

1) Create virtual environment with your python version of choice 

2) Activate environment 

3) Run `make exmaples` to set up exampels for testing

4) Run `pytest tests/example_tests` to run all the tests 

5) When tests are completed, you can run `make clean_examples` to clean up. 

Note that when pytest is installed, executable might be installed with the version of python loaded during installation. You can modify this via runnign `which pytest` and then modifying the shebang `#` to read form the desired environment. If you'd like pytest to reuse the loaded virtual environment, something like `#!/usr/bin/env python3` should work well for you. 