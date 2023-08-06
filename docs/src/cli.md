
lolpop comes equipped with a CLI tool that is a swiss army knife with many different uses. Among its key capabilities are: 

1. The ability to run lolpop workflows in an operational capacity. 

2. Generating extension templates. 

3. Automatically generating tests and documentations for extensions. 

4. Testing workflows given proper testing configuration. 

5. Running arbitrary custom CLI extensions.

... and more! As you can install your own CLI extensions to use with the lolpop CLI, the sky is really the limit to what you can accomplish with the lolpop CLI. 

## Installing 

The lolpop CLI is installable as a lolpop extra package. In particular, you'll want to run the following: 

```python
pip3 install `lolpop[cli]`
```

You can verify that installation was successful via: 

```bash
lolpop --version 
``` 
which should spit out which version of lolpop you have installed. 

## Troubleshooting 

Assuming you successfully pip installed lolpop and you expect `lolpop --version` to work, it's disheartening to see an error message like: 

```console
> lolpop --version
Traceback (most recent call last):
  File "/Users/jordanvolz/venv/lolpop/bin/lolpop", line 3, in <module>
    from lolpop.cli.cli import app 
ModuleNotFoundError: No module named 'lolpop'
```
But fear not. The above is very likely an indication that the python environment that you installed lolpop into is not the same one that you are running it from. That is -- perhaps lolpop was installed into a virtual environment that you are not currently active in. If you inspect the file in question, it should contain a comment that points to a python environment. This should give you a good indication of which environment lolpop was installed into, and you can check what you're currently using via `which python3`. 

In the event that you get a command not found error for lolpop, ala: 

```
> lolpop --version
zsh: command not found: lolpop
```

This is likely an indication that lolpop was installed into a directory that is not on your system `PATH`. To troubleshoot, check `echo $PATH` to see what directories are searched by default and you can use the `find` command to figure out where lolpop was installed (i.e. `find / -name lolpop`) -- although it's very likely that lolpop will be installed user `/usr/bin`, `/usr/bin/local`, or in the path of a virtual envrionment. Once you've identified the discrepency, either update your `PATH` variable in your `~/.bash.rc` file or add an alias for lolpop. 





## In this Section 

- [CLI User Guide](cli_guide.md): User Guide for using the CLI. 

- [CLI Reference](cli_reference.md): Reference documentation for using the CLI. 

Also see: 

- [CLI Extensions](extending_cli.md): Documentation on using CLI extensions. 

