import configparser


def configExtract(c, section):
    d = {}
    options = c.options(section)
    for o in options:
        try:
            d[o] = c.get(section, o)
        except:
            d[o] = None
    return d
