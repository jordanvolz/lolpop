
Writing tests for your extensions is a good practice. Tests are good. Tests are, in fact, *great*. Writing tests, however, is kind of boring and can be a drag. With lolpop, you can quickly automate writing tests for your extensions with generative AI. 

## Automating Extension Unit Tests

The lolpop [cli](cli.md) has a method that users can use to generate tests for an extension class. Invoking it is farily straightforward. Simply execute the following: 

```bash 
lolpop create tests <source_file> <class_name> --output-path my_extension_tests.py
```

The above command will write tests for the given extension `class_name` in the provided `source_file` and save the resulting tests to the `--output-path`. 

!!! Note
    Generative AI is far from perfect. Maybe someday it will truly master human-machine communication. As such, we'd expect your tests to be about ~80% correct on average. You'll definitely want to review your tests and modify them accordingly before accepting them, but we do think this is a huge productivity boost to writing tests from scratch. In our own experimentation, we've been pretty happy and often impressed with the breath and depth of tests that can surface from a quick CLI command. 

### Customizing Test Generation

By default, lolpop will use OpenAI's chatGPT to generate `pytest` tests for every method in the provided class. This can be customized with several options on this command, like `--method-filter`, `--generator-class`, and `testing-framework`. 

Like many of lolpop's CLI commands, the `lolpop create tests` command is pluggable, meaning that users can create their own class to process the request to generate tests and utilize this within the CLI without having to modify the CLI code itself. By default, `lolpop create tests` utilizes the `OpenAIChatbot` class. If users have a preference in what generative AI technology is used, they can easily create their own chatbot [extension](extensions.md) and swap this in via the `--generator-class` option when invoking `lolpop create tests`. 

## Writing Workflow Tests 

In general, it is also good practice to incorporate your new extension in some [workflow tests](testing_workflows.md). We don't yet have a handle using generative AI to automate this task yet, but we anticipate doing so once we have a suitable body of integrations and extension from which to train on. 
