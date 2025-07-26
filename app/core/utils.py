from slugify import slugify as _slugify

def slugify(name: str) -> str:
    return _slugify(name.lower())
