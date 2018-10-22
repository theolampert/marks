from urllib.parse import urlparse


def strip_protocol(url):
    parsed = urlparse(url)
    return parsed.netloc + parsed.path + parsed.query
