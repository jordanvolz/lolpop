

## Naming Conventions: 

- Methods without a leading underscore: public methods. It's expected that these can be accessed by parent or peer resources. Example: `get_data`

- Methods with a leading underscore: protected methods. A method that can be used by the class itself and `parent` resources, but should not be used by peer resources. Example: `_load_data` 

- Methods with two leading underscores: private methods. Should only be used by the class itself. example `__do_something`

Note: private/protected functions don't get their execution logged by default. 

## args & kwargs

You should always include args and kwargs in your methods, even if you don't use them (and you often won't). This helps with a lot of stuff like inheritance and making it easy to switch components in a workflow, etc. 

## In This Section 

- [Extending Integrations](extending_integrations.md): Learn how to create an extension. 

- [Building Extensions from Templates](extension_templates.md): Learn how to build an extension from a template. 

- [Packaging Extensions](packaging_extensions.md): Learn how to package an extension.

- [Running Extensions](running_extensions.md): Learn how to run an extension. 

- [Writing Tests](extensions_tests.md): Learn how to write tests for an extension.

- [Generating Documentation](documentation.md): Guidelines for extension Documentation. 

- [Extending the CLI](extending_cli.md): Learn how to write CLI extensions. 