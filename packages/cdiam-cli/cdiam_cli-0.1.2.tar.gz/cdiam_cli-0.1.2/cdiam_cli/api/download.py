import click
import requests
from urllib.request import urlopen
from .settings import read_api_endpoint, read_api_token


@click.command()
@click.argument("object_id", type=str)
def download_data(object_id: str):
    """This api download data of given object_id"""
    res = requests.get(
        f"{read_api_endpoint()}/data/data/download-file/{object_id}",
        cookies={"cdiam_session_token": read_api_token()},
    )

    if res.status_code != 200:
        print(res.json())
    else:
        for url in res.json()["url"]:
            response = urlopen(url)
            file_name = response.headers.get_filename()
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(file_name, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
