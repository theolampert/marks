from urllib.parse import urlparse


def strip_protocol(url):
    parsed = urlparse(url)
    return parsed[1] + parsed[2] + parsed[3]

