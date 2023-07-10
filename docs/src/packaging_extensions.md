Once your extension is completely built, you may wish to easily package it so it can be quickly deployed by others. Read on to learn how to do that with lolpop.  


## Packing An Extension with Poetry 

If you're using a [lolpop project](lolpop_projects.md) to build your extension, you'll be happy to know that this already is integrated with [poetry](https://python-poetry.org) to enable easy packaging of the extension. 

If you're new to poetry, be sure to check ou their [docs](https://python-poetry.org/docs/basic-usage/), but the MVP process here entails: 

1. Modifying `pyproject.toml` in your project directory to include any metadata you want for your project. At the very least, you should add any library dependencies for your extension in `[tool.poetry.dependencies]`. 

2. Build your package via `poetry build`. This will build your extension as a tarball and wheel. 

And that's it! You'll now have a nice artifact which you can use to share your extension. 

## Installing An Extension 

Assuming you're properly built an extension and now have a tarball of that extension, you can easily install this extension where you'd like via: 

```python
pip3 install /path/to/my_extesnion.tar.gz
```


## Publishing Extensions for Consumption 

If you want to take it one step further, you can even try uploading your extension on a package index like [PyPI](https://pypi.org). This will allows others to `pip install` your package over the Internet without having to download anything first. The steps are more involved that we'd like to cover here, but there are many [good guides online](https://www.digitalocean.com/community/tutorials/how-to-publish-python-packages-to-pypi-using-poetry-on-ubuntu-22-04) to help with the process. 

Once you've sorted out the details, you can easily publish updates to your extension via: `poetry publish`. 

!!! Note
    Of course, if you've gone this far with your extension, you should also consider [contributing](contributing.md) it to be part of the main lolpop code base. 