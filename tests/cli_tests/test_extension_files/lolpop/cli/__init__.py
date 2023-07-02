from pkgutil import extend_path

#allows extensions to work when doing local dev and adding them to sys path
__path__ = extend_path(__path__, __name__)
