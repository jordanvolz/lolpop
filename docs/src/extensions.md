

## Conventions
### Naming Conventions: 

- Methods without a leading underscore: public methods. It's expected that these can be accessed by parent or peer resources. Example: `get_data`

- Methods with a leading underscore: protected methods. A method that can be used by the class itself and `parent` resources, but should not be used by peer resources. Example: `_load_data` 

- Methods with two leading underscores: private methods. Should only be used by the class itself. example `__do_something`

Note: private/protected functions don't get their execution logged by default. 

### args & kwargs

You should always include args and kwargs in your methods, even if you don't use them (and you often won't). This helps with a lot of stuff like inheritance and making it easy to switch components in a workflow, etc. 

## In This Section 

- [Building Extensions](building_extensions.md): Learn how to build an extension from a template. 

- [Using Extensions](using_extensions.md): Learn how to use an extension. 

- [Packaging Extensions](packaging_extensions.md): Learn how to package an extension.

- [Writing Tests](writing_extension_tests.md): Learn how to write tests for an extension.

- [Generating Documentation](writing_extension_documentation.md): Guidelines for extension Documentation. 

- [Extending the CLI](extending_cli.md): Learn how to write CLI extensions. 