"""
jw_download.task
================

All task of jw_download.
"""

import sys
import functools
from hashlib import md5
from collections import namedtuple

import requests
from tqdm import tqdm
from yaspin import yaspin


def spinned(func):
    """
    Decorator to show spinner on terminal.
    """

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        name = func.__name__.replace("_", " ")

        with yaspin(text=name, color="blue") as spinner:
            try:
                result = func(*args, **kwargs, spinner=spinner)
                spinner.ok(">")
                return result
            except Exception as error:
                spinner.fail("Error |")
                spinner.write(str(error))
                sys.exit(1)

    return wrapped


@spinned
def fetch_api(**params):
    api_url = "https://b.jw-cdn.org/apis/pub-media/GETPUBMEDIALINKS"

    params = {
        "issue": params["issue"],  # Publication date format: {year}{month}
        "output": "json",  # Result format
        "pub": params["pub"],  # publication codename
        "fileformat": params["fileformat"],
        "alllangs": 0,  # I don't know about this
        "langwritten": params["lang"],  # File language
        "txtCMSLang": params["lang"]
    }

    r = requests.get(api_url, params)

    return r.json()


@spinned
def get_downloadable_file(api_result, spinner):
    File = namedtuple("File", ["url", "checksum"])
    try:
        language = list(api_result["languages"])[0]
    except TypeError:
        spinner.write("> No result")
        return []

    result = []
    for fileformat in api_result["fileformat"]:
        try:
            for f in api_result["files"][language][fileformat]:
                result.append(
                    File(
                        url=f["file"]["url"],
                        checksum=f["file"]["checksum"]
                    )
                )
        except KeyError:
            pass
    return result


@spinned
def download(url, checksum, filepath, spinner):
    if filepath.exists():
        if check_file(filepath, checksum):
            spinner.write("> Success")
            return True
        
        filepath.unlink()

    filepath.touch()
    spinner.write(f"> Downloading {url}")
    spinner.write("> Get filesize")
    file_size = int(requests.head(url).headers["Content-Length"])
    spinner.write(f"> Filesize: {round((file_size/1024)/1024, 2)}Mb")
    spinner.hide()
    pbar = tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024)
    req = requests.get(url, stream=True)

    with filepath.open(mode="wb") as fp:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                fp.write(chunk)
                pbar.update(1024)

    pbar.close()
    spinner.show()
    return download(url, checksum, filepath)


@spinned
def check_file(filepath, checksum, spinner):
    content = filepath.read_bytes()
    filesum = md5(content).hexdigest()

    if filesum == checksum:
        return True

    spinner.write("> Wrong checksum (redownloading)")
    return False
