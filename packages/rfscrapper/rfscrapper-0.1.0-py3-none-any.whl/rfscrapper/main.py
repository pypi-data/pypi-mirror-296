import sys
import os
from tqdm import tqdm
from .rf_scrapper import (
    API_URL_PATTERN,
    INPUT_URL_PATTERN,
    save_podcast,
    get_podcast_name,
    get_podcast_api_url,
)


def cli() -> None:
    base_dir = os.path.dirname(__file__)
    os.chdir(base_dir)
    if len(sys.argv) > 1:
        if len(sys.argv) == 3:
            folder_path = sys.argv[2]
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
        else:
            folder_path = None
        link_argv = sys.argv[1]
        if ".txt" in link_argv:
            skipped_urls = []
            with open(link_argv) as fp:
                if folder_path is not None:
                    os.chdir(folder_path)
                for line in tqdm(fp.readlines()):
                    line = line.rstrip("\n")  # remove url encoding newline
                    if INPUT_URL_PATTERN.match(line):
                        download_url = get_podcast_api_url(line)
                        filename = get_podcast_name(line)
                        save_podcast(filename, download_url)
                    else:
                        skipped_urls.append(line)
            if skipped_urls:
                print("The following URLs have been ignored because they are invalid: ")
            for url in skipped_urls: print(url)
        elif INPUT_URL_PATTERN.match(link_argv):
            if folder_path is not None:
                os.chdir(folder_path)
            download_url = get_podcast_api_url(link_argv)
            filename = get_podcast_name(link_argv)
            save_podcast(filename, download_url)
        else:
            print("The given url is invalid.")
    else:
        print(
            """Please provide a link to your podcast or the path to a list of links.
For more infos checkout the README."""
        )
