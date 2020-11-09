import sys
import functools
from hashlib import md5
from collections import namedtuple

import requests
from tqdm import tqdm
from yaspin import yaspin


def spinned(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        name = func.__name__.replace("_", " ")

        with yaspin(text=name, color="blue") as sp:
            try:
                result = func(*args, **kwargs, sp=sp)
                sp.ok(">")
                return result
            except Exception as e:
                sp.fail("Error |")
                sp.write(str(e))
                sys.exit(1)

    return wrapped


@spinned
def fetch_api(**params):
    API_URL = "https://b.jw-cdn.org/apis/pub-media/GETPUBMEDIALINKS"

    params = {
        "issue": params["issue"],  # Publication date format: {year}{month}
        "output": "json",  # Result format
        "pub": params["pub"],  # publication codename
        "fileformat": params["fileformat"],  # file format separated with comma, Supported fileformat: PDF, EPUB, JWPUB, RTF, TXT, BRL, BES, DAISY
        "alllangs": 0,  # I don't know about this
        "langwritten": params["lang"],  # File language
        "txtCMSLang": params["lang"]
    }

    r = requests.get(API_URL, params)

    return r.json()


@spinned
def get_downloadable_file(api_result, sp):
    File = namedtuple("File", ["url", "checksum"])
    try:
        language = list(api_result["languages"])[0]
    except TypeError:
        sp.write("> No result")
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
def download(url, checksum, filepath, sp):
    if filepath.exists():
        if check_file(filepath, checksum):
            sp.write("> Success")
            return True
        else:
            filepath.unlink()

    filepath.touch()
    sp.write(f"> Downloading {url}")
    sp.write("> Get filesize")
    file_size = int(requests.head(url).headers["Content-Length"])
    sp.write(f"> Filesize: {round((file_size/1024)/1024, 2)}Mb")
    sp.hide()
    pbar = tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024)
    req = requests.get(url, stream=True)

    with filepath.open(mode="wb") as fp:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                fp.write(chunk)
                pbar.update(1024)

    pbar.close()
    sp.show()
    download(url, checksum, filepath)


@spinned
def check_file(filepath, checksum, sp):
    content = filepath.read_bytes()
    filesum = md5(content).hexdigest()

    if filesum == checksum:
        return True
    else:
        sp.write("> Wrong checksum (redownloading)")
        return False
