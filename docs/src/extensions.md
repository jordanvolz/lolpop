
lolpop is a modular framework which expects that users will want or need to create their own extensions of core functionality. This could include creating new *components*, *pipelines*, and *runners*, as well as introducing new operational functionality via [cli extensions](extending_cli.md). 

Integration extensions can either be new implementations of an existing implementation type (such as creating a new `metadata_tracker`) or an entirely new type which does not exist yet (such as `vector_database`). lolpop's implementation is very open ended and can accommodate a variety of scenarios. 

In this section we'll give an overview of working with extensions and subsequent sections will dive down deeper into important topics. 

## Overview of Creating an Extension

When creating an extension, we advise the following steps: 

1. Create a new extension via an [existing template](building_extensions.md#creating-extensions-via-templates)].

2. Modify the base integration class file (i.e. `base<integration_type>.py`)by providing an interface that you would expect all integrations of this type to implement. 

3. The methods in your base integration need not do anything. Anything that implements the base class should implement their own methods. There may also be cases where certain methods are shared amongst implementations. If that's the case, you would want to implement those methods directly in the base integration class. Anything inheriting from this class in the future always has the option to override the default implementation anyway. 

4. Now you can modify the integration class file (i.e. `<integration>.py`). You'll want to implement any and all methods from the base class which you'll need for your workflow. You additionally may wish to include `__REQUIRED_CONF__` and `__DEFAULT_CONF__` to help guide users to working with your integration. 

5. When you are finished with your integration, don't forget to write [tests](writing_extension_tests.md) and [documentation](writing_extension_documentation.md)! 

6. When you are all finished, be sure to modify your `pyproject.toml` with any dependencies and then you can [package up your extension](packaging_extensions.md) for use. 

## Conventions

There are no real limitations to what you can do in an extension, and we expect that many organizations will have standardized best practices around creating code, etc. In the absence of any internal guidance, we propose the following conventions to keep in mind when developing extensions. 

### Method Naming Conventions: 

- Methods without a leading underscore are considered *public methods*. It's expected that these can be accessed by parent or peer resources. This should be the majority of methods defined and used in base integration classes. Example: `get_data`

- Methods with a leading underscore (`_`) are considered protected methods. These are methods that can be used by the class itself and `parent` resources, but should not be used by peer resources. Since they are accessed outside the class itself, they should also be included in base integration classes as all integrations of this type should have this method implemented. Example: `_load_data` 

- Methods with two leading underscores (`__`) are considered private methods. These should only be used by the class itself and should not be accessed by any other methods. As such, they are not defined in base integration classes.  Example: `__do_something`

!!! Note
    Private and protected methods don't get their execution logged by default. 

### args & kwargs

You should always include `*args` and `**kwargs` in your methods, even if you don't use them (and you often won't). This helps with a lot of stuff like inheritance and making it easy to switch between integrations in a workflow, etc. I.E. one integration may take 4 keywords, and another takes 2. By using `**kwargs` we're able to capture all the input to a method properly without incurring signature errors when switching integrations, and each integration can ignore what it doesn't need. 

## In This Section 

- [Building Extensions](building_extensions.md): Learn how to build an extension from a template. 

- [Using Extensions](using_extensions.md): Learn how to use an extension. 

- [Packaging Extensions](packaging_extensions.md): Learn how to package an extension.

- [Writing Tests](writing_extension_tests.md): Learn how to write tests for an extension.

- [Generating Documentation](writing_extension_documentation.md): Guidelines for extension Documentation. 

- [Extending the CLI](extending_cli.md): Learn how to write CLI extensions. 