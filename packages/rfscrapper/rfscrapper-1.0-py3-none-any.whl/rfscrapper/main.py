from pathlib import Path
from argparse import ArgumentParser
from re import compile
from tqdm import tqdm
from .rf_scrapper import (
    save_podcast,
    get_podcast_name,
    get_podcast_api_url,
)


INPUT_URL_PATTERN = compile(
    "^https:\/\/www\.radiofrance\.fr\/(franceculture|franceinter)\/podcasts.*[0-9]{7}$"
)


def convert_path(path) -> Path:
    """
    Join a given path with the current working directory to create an absolute path.
    
    Notes:
        If the input path is already an absolute path, it is returned as is.
"""
    return Path.cwd() / path


def create_parser() -> ArgumentParser:
    """Creates a parser wich takes 2 arguments : podcasts (required) and output (optionnal)."""
    parser = ArgumentParser(
        prog="rfscrapper",
        description="A simple CLI wich downloads podcasts from radiofrance."
    )
    parser.add_argument(
        "podcasts",
        help="Must either be a link to the podcast you want to download or the path to a file were each line is a link."
    )
    parser.add_argument(
        "-o", "--output",
        type=convert_path,
        default=".",  #  current directory
        help="The output folder in which you want to put your downloads. By default, it is s the current folder directory."
        )
    return parser


def cli() -> None:
    """Contains all the logic of the cli."""
    parser = create_parser()
    args = parser.parse_args()
    podcast_reference: str = args.podcasts
    output_folder: Path = args.output
    output_folder.mkdir(exist_ok=True)
    if podcast_reference.endswith(".txt"):
        podcast_reference: Path = convert_path(podcast_reference)
        skipped_urls = []
        with open(podcast_reference) as fp:
            for line in tqdm(fp.readlines()):
                line = line.rstrip("\n")  # remove url encoding newline
                if INPUT_URL_PATTERN.match(line):
                    download_url = get_podcast_api_url(line)
                    file_path = convert_path(output_folder/get_podcast_name(line))
                    save_podcast(file_path, download_url)
                else:
                    skipped_urls.append(line)
        if skipped_urls:
            print("The following URLs have been ignored because they are invalid: ")
        for url in skipped_urls: print(url)
    elif INPUT_URL_PATTERN.match(podcast_reference):
        download_url = get_podcast_api_url(podcast_reference)
        file_path: Path = convert_path(output_folder/get_podcast_name(podcast_reference))
        save_podcast(file_path, download_url)
    else:
        print("error: The given url is invalid")
