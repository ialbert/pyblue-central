__author__ = 'ialbert'

def keep(name):
    return name.endswith("png")

def gallery(items):
    out = [ ]
    items = filter(keep, items)
    for item in items:
        out.append(item)
    return out