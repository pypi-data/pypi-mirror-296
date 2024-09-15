# Welcome to radiofrance scraper CLI

A simple CLI that downloads one or more podcasts from <https://www.radiofrance.fr/>.

I made this script because users are not allowed to download all podcasts on mobile.

You can then transfer your favourite podcasts to your phone to listen to them offline!

## How to

Install rfscrapper by running this comand:

```batch
pip install rfscrapper
```

You can run rfscrapper with 2 arguments:

1. Must either be a link to the podcast you want to download or the path to a file were each line is a link. A new line is created each time you press the Enter key, so don't be fooled by the notepad when it displays the link you just pasted over two lines!
2. The output folder in which you want to put your downloads. By default, it is s the current folder directory.

For example..

```batch
rf_scrapper "put here a link in brackets"
```

or

```batch
rf_scrapper "list.txt" -o "output_folder"
```

are both correct ways to launch the CLI !
