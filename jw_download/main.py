from pathlib import Path

import click

from .task import fetch_api, get_downloadable_file, download
from .config import Config


conf = Config()


@click.command()
@click.option('--date', default=conf.date, show_default=True)
@click.option('--pub', default=conf.pub, show_default=True, help="Publication codename")
@click.option('--fileformat',
              default=conf.fileformat,
              show_default=True,
              help="Comma separated file format")
@click.option('--lang', default=conf.lang, show_default=True)
@click.argument('dest',
                default=conf.dest,
                nargs=1,
                type=click.Path(file_okay=False,
                                writable=True,
                                resolve_path=True))
def main(date, pub, fileformat, lang, dest):
    """
    JW book downloader.
    """

    params = {
        "issue": date,
        "pub": pub,
        "fileformat": fileformat.upper().strip(),
        "lang": lang,
    }

    dest = Path(dest)

    api_result = fetch_api(**params)
    result = get_downloadable_file(api_result)

    for f in result:
        filename = f.url.split("/")[-1]
        filepath = dest / filename
        download(f.url, f.checksum, filepath)
