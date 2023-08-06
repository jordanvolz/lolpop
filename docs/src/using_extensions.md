
If you're building a new extension from scratch or trying to use someone else's extension, you may wonder what is the proper way to use an extension. In this section we'll cover how to do exactly that. 

## Working With Extensions

There are two main ways you may wish to work with an extension: either directly in code, as may be the case with a runner, or in configuration, which is likely the case with components and pipelines. 

### Using Extensions in Code 

You can refer to an extension in code by importing the extension class from `lolpop.extension` as seen below: 

```python
from lolpop.extension import SomeExtension

some_config = {...}

some_extension = SomeExtension(conf=some_config)
```

Note that this assumes your extension class is discoverable, which means it was [packaged and installed](packaging_extensions.md) or is [configured locally](using_extensions.md#local-development-with-extensions)


### Using Extension in Configurations

When referring to an extension in a configuration file, you need only provide the relevant extension class in the configuration. lolpop knows to search both built-in integrations, as well as any extension paths to resolve class names. 

Again, note that this assumes your extension class is discoverable, which means it was [packaged and installed](packaging_extensions.md) or is [configured locally](using_extensions.md#local-development-with-extensions)

## Local Development with Extensions

When building your own extensions it's very likely that you'll want to leverage built-in lolpop components along with the extension that you're currently working on. To enable lolpop to recognize your extension, you simply need to add your project directory to the `PYTHONPATH` variable. This will allow lolpop to discover your extension and it can then be used in configuration or directly in python code. 

In particular, make sure to do something like the following: 

```bash 
export PYTHONPATH=$PYTHONPATH:/path/to/project/project_name
```

You can troubleshoot any issues you may have discovering your extension path by checking the contents of `sys.path` to ensure that the correct directory is listed.

