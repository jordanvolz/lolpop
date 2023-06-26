lolpop contains a lightweight workflow testing framework. 

We'd love to make this pluggable/extensible, and may in the future! One big gripe we had while making this is that there do not seem to be many (any?) well-defined testing frameworks for arbitrary ML workflows. Most testing frameworks are strictly *data* related. While these are certainly useful, they leave a lot on the table in terms of testing surface area. 

In this section we'll cover the built-in framework. Feel free to contact us with suggestions if you prefer a method different than the one outlined below. 

## How Tests Works
We tried to design test to be conceptually simple and also very flexible. The gist is as follows: 

1. For any method in any runner, pipeline or component, you can attach a test to it. 
2. Tests can either be run before the method executes or after the method executes. 
3. Tests are written in python. You can write as many tests as you want for each method. 
4. You run a special workflow to execute tests on your methods. Lolpop will run the tests and spit out your results. 
5. Tests are specified in a special configuration file. Like everything else, you can maintain different configuration files to test different scenarios for your workload. 

And that's it. Simple, right? 

Tests are essentially pre- and post-hooks into your methods. Both pre- and post-hooks will receive all arguments to the method as input, and post-hooks will also receive the outputs of the method itself. 

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

Tests should be small and atomic. The more complex a test is, the more ways where it can unexpected fail and this makes troubleshooting and debugging difficult. Try to keep tests small and reusable. You'll likely find that any test you write can be applied to many use-cases, so try to make them generic. 

Tests should return a boolean value, i.e. `True` of `False` indicating whether or not the test succeeded. 
The name of the file containing the test corresponds to the test name, and the method to use for the test should be `test`. For example, here is a small tests that checks if the model target has non-trivial amounts of labels for a classification problem: 

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
    pre-hooks: [/path/to/test1.py]
    post-hooks: [/path/to/test2.py, /path/to/test2.py] 
```
Both pre- and post-hooks are optional. You don't need to test every method, and some you may just want to do one vs the other. You can provide many tests to a method via adding more files to the list to attach to the method. 

Here's an example of a larger test configuration: 

```yaml title="workflow_test.yaml" 
#runner-specific tests
tests: 
  train:
    pre-hooks: [tests/test_resource_availability.py]

#pipeline-specific tests
process: #pipeline 
  tests: # pipeline tests
      train_model: 
        post-hooks: [tests/test_model_perf.py] 
  data_transformer: #component
    tests: #local component tests 
        process_data:
          pre-hooks: [tests/test_data_non_null.py, tests/test_data_size.py]
          post-hooks: [tests/test_check_label_counts.py]

#global component tests 
metadata_tracker:
  tests: 
    log_artifact:
      post-hooks: [tests/test_artifact_exists.py] 

```

## Running Tests

Tests can be run via the lolpop [CLI](cli.md). Users need only invoke the `test workflow` command with proper arguments and lolpop will handle the rest. 

Here's an eample of testing a workflow: 

```bash 
lolpop test workflow MyRunner dev.yaml workflow_test.yaml
``` 

lolpop will then attach your tests to all specified methods and run the workflow, outputting all tests results. 