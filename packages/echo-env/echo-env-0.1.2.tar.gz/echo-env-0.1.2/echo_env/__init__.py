from accessors import Branch, Bundle


def __getattr__(name):
    if name == '__getattr__':
        raise ImportError("Illegal item")

    return globals()[name]
  
