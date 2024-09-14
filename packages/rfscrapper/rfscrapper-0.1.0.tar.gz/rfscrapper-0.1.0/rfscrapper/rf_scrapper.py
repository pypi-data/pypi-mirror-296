import requests
from re import compile


API_URL_PATTERN = compile("https://media\.radiofrance-podcast\.net\/(?!.*\.m4a).*?\.mp3")
INPUT_URL_PATTERN = compile(
    "^https:\/\/www\.radiofrance\.fr\/(franceculture|franceinter)\/podcasts.*[0-9]{7}$"
)


def save_podcast(filename, link) -> None:
    with requests.get(link, stream=True) as response:
        response.raise_for_status()
        with open(filename, "wb") as fp:
            for chunk in response.iter_content(chunk_size=8192):
                fp.write(chunk)


def get_podcast_name(url) -> str:
    url = url.split("/")
    url = "-".join(url[5:])
    url = url.split("-")
    url = url[:-1]
    url = "-".join(url)+".mp3"
    return url


def get_podcast_api_url(url):
    response = requests.get(url)
    response.raise_for_status()
    result = API_URL_PATTERN.search(response.text)
    if result:
        return result[0]
    else:
        raise Exception(
f"""Failed to get the download url for the given url: 
{url}
"""
        )
