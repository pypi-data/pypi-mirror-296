import pathlib
import tempfile


def cache_file_for_url(url):
    stem = url.split("/")[-1]
    return pathlib.Path(tempfile.gettempdir()) / f"{stem}.htm"


def icase_key_get(d, key):
    for variant in (key, key.upper(), key.lower()):
        try:
            return d[variant]
        except KeyError:
            pass
        raise
