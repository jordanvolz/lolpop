lolpop contains a lightweight workflow testing framework. 

We'd love to make this pluggable/extensible, and may in the future! One big gripe we had while making this is that there do not seem to be many (any?) well-defined testing frameworks for arbitrary ML workflows. Most testing frameworks are strictly *data* related. While these are certainly useful, they leave a lot on the table in terms of testing surface area. 

In this section we'll cover the built-in framework. Feel free to contact us with suggestions if you prefer a method different than the one outlined below. 

## How Tests Works
lolpop tests were designed to be conceptually simple and also very flexible. The gist is as follows: 

1. For any method in any runner, pipeline or component, you can attach a test to it. 
2. Tests can either be run before the method executes or after the method executes. 
3. Tests are written in python. You can write as many tests as you want for each method. 
4. You run a special workflow to execute tests on your methods. Lolpop will run the tests and spit out your results. 
5. Tests are specified in a special configuration file. Like everything else, you can maintain different configuration files to test different scenarios for your workload. 

And that's it. Simple, right? 

Tests are essentially pre- and post-hooks into your methods. Both pre- and post-hooks will receive all arguments to the method as input, including the integration object, and post-hooks will also receive the outputs of the method itself. 

The main idea here is to provide a quick framework for testing various scenarios for your workload. I.E. maybe you wish to maintain a "golden dataset" for which you expect a certain model performance. The lolpop testing framework would allow you to easily test changes to the workflow on this dataset and raise an error if performance didn't meet a certain threshold. Then, this test could be hooked into a CI/CD process that run on any new PR to ensure that the performance threshold has been met. In this way, it should be simple to design a variety fo tests for all kinds of scenarios you wish to check.

## Writing Tests

Tests are written in python and attached to existing methods in your workflows. Tests can be one of two types: pre-hook or post-hook. Pre-hooks take the following as input `obj`, `args`, `kwargs`, where `obj` is the parent object and `args` and `kwargs` are the same arguments and keyword arguments passed into the attached method. Post-hooks have input as `obj`, `output`, `args`, `kwargs`, where `ouput` is the output of the attached function. 

=== "Pre-hook test" 
    ```python
    def test(obj, *args, **kwargs):
        # do something here
        return True
    ```
=== "Post-hook test"
    ```python
    def test(obj, data, *args, **kwargs):
        # do something here
        return True
    ```

Tests should be small and atomic. The more complex a test is, the more ways where it can unexpectedly fail and this makes troubleshooting and debugging difficult. Try to keep tests small and reusable. You'll likely find that any test you write can be applied to many use-cases, so try to make them generic. 

Tests should return a boolean value, i.e. `True` of `False` indicating whether or not the test succeeded. Optionally, Tests may additionally return a string value that can be used to explain some aspect of the test. This is meant to cover complex cases where a simple `True`/`False` value is insufficient. 

=== "Pre-hook test returning a description" 
    ```python
    def test(obj, *args, **kwargs):
        # do something here
        return (True, "My Description")
    ```
=== "Post-hook test returning a description"
    ```python
    def test(obj, data, *args, **kwargs):
        # do something here
        return (True, "My Description")
    ```

The test name is determined by `name_of_file.name_of_method`. By default, lolpop will look for a method called `test`, but users can specify the method name for use in a particular test. This handles use cases where you may wish to include many tests in the same file. For example, here is a small tests that checks if the model target has non-trivial amounts of labels for a classification problem: 

```python title="test_check_label_counts.py"
def test(obj, data, *args, **kwargs):
    target = obj._get_conf("model_target")
    return data[target].nunique() > 1
```

It's important to note that the `obj` file is passed into all tests, so users have access to any runner/pipelines/components that the attached method would have access to as well. This is likely most useful in retrieving configuration passed into the workflow, which may also be of use to and affect the results of the test. 

## Test Configuration 

Once tests have been written, you need to attach tests to methods in your workflow. You can do this by simply adding the following to any runner, pipeline, or component configuration: 

```yaml title="sample test configuration"
tests: 
  method_name:
    pre-hooks: 
        - hook_file: /path/to/test1.py
          hook_method: test_something
    post-hooks: 
        - hook_file: /path/to/test2.py
          hook_method: another_test
        - hook_file: /path/to/test2.py
          #no hook_method means we'll use method 'test'
```
Both pre- and post-hooks are optional. You don't need to test every method, and some you may just want to do one vs the other. You can provide many tests to a method via adding more files to the list to attach to the method. 

Here's an example of a larger test configuration: 

```yaml title="workflow_test.yaml" 
#runner-specific tests
tests: 
  train:
    pre-hooks: 
        - hook_file: tests/test_resource_availability.py

#pipeline-specific tests
process: #pipeline 
  tests: # pipeline tests
      train_model: 
        post-hooks: 
            - hook_file: tests/test_model_perf.py 
  data_transformer: #component
    tests: #local component tests 
        process_data:
          pre-hooks: 
            - hook_file: tests/test_data_non_null.py 
            - hook_file: tests/test_data_size.py
          post-hooks: 
            -hook_file: tests/test_check_label_counts.py

#global component tests 
metadata_tracker:
  tests: 
    log_artifact:
      post-hooks: 
        - hook_file: tests/test_artifact_exists.py 

```

### Optional Components
There are two special optional components that can be provided in test configuration: `test_logger` and `test_recorder`. 

`test_logger` is a normal `logger` component that the testing framework will use to log test results to. If no logger is provided, it will simply log out to the same logger as the provided integration that is being tested. This might be useful if you wish to log all your test results separately from your integration logs. 

`test_recorder` is a component that keeps track of all tests during a test run. By default, lolpop will use the `LocalTestRecorder`. When running a test this will keep track of all results and print a summary at the end of the run. We can imagine that some users way wish to make their own `test_recorders` to customize the way that test reports are generated. 

The configuration for these two components would look something like this within a the test configuraiton. 

```yaml title="test configuration with test_logger and test_recorder"
components:
  test_logger: FileLogger
  test_recorder: MyTestRecorder
test_logger: 
  config: 
    log_filename: lolpop_tests.log
test_recorder: 
  config: 
    key: value
    ... 

```

## Running Tests

Tests can be run via the lolpop [CLI](cli.md). Users need only invoke the `test workflow` command with proper arguments and lolpop will handle the rest. 

Here's an example of testing a workflow: 

```bash 
lolpop test workflow MyRunner workflow_test.yaml --integration-config dev.yaml --build-method process_data
``` 

lolpop will then attach your tests to all specified methods and run the workflow, outputting all tests results. 

If you're using the default `LocalTestRecorder` you'll get a summary test report at the conclusion of the workflow. Something akin to: 

```bash 
> lolpop test workflow BaseModelTrainer tests/cli_tests/test_workflow_files/test_conf.yaml --integration-type component --build-method fit --build-args 'hello world!'
Loaded BaseModelTrainer!
Constructing test plan from configuration: tests/cli_tests/test_workflow_files/test_conf.yaml
2023/07/03 03:40:05.154146 [INFO] <LocalTestRecorder> ::: Loaded class StdOutLogger into component logger
2023/07/03 03:40:05.155980 [INFO] <LocalTestRecorder> ::: Loaded class StdOutNotifier into component notifier
2023/07/03 03:40:05.156088 [INFO] <LocalTestRecorder> ::: Unable to load metadata_tracker component.
Test plan built! Found 1 method(s) to test
Initializing class BaseModelTrainer with config file tests/cli_tests/test_workflow_files/test_conf.yaml
2023/07/03 03:40:05.164864 [INFO] <BaseModelTrainer> ::: Unable to load metadata_tracker component.
Initialized!
Applying test plan to class BaseModelTrainer
Test plan applied!
Executing BaseModelTrainer.fit with args ['hello world!'] and kwargs {}
2023/07/03 03:40:05.170670 [DEBUG] <BaseModelTrainer> ::: Running pre-hook prehook_success.test
2023/07/03 03:40:05.170786 [INFO] <BaseModelTrainer> ::: Pre-hook prehook_success.test passed.
2023/07/03 03:40:05.170877 [DEBUG] <BaseModelTrainer> ::: Pre-hook prehook_success.test finished.
2023/07/03 03:40:05.170965 [DEBUG] <BaseModelTrainer> ::: Running post-hook posthook_failure.test
2023/07/03 03:40:05.171093 [WARN] <BaseModelTrainer> ::: Post-hook posthook_failure.test failed
2023/07/03 03:40:05.171181 [DEBUG] <BaseModelTrainer> ::: Post-hook posthook_failure.test finished.
Workflow completed!

Printing Test Report: 
Method: BaseModelTrainer.fit
         Test: prehook_success.test
         Passed: True
         Test: posthook_failure.test
         Passed: False
```