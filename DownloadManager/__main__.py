import threading
from time import sleep
import pyfiglet
import readline

import os

from DownloadManager.utils.colors import (
    cBold,
    cBlue,
    cEnd,
    cMagenta,
    show_cursor,
    magic_char,
)
from DownloadManager.utils.downloader import add_download_link, print_downloader
from DownloadManager.utils.helpers import (
    remove_duplicate_links,
    show_post_download_stats,
)
from DownloadManager.vars import Vars
from DownloadManager import aria2


def show_downloader():
    while True:
        if len(Vars.active_downloads) != 0:
            downloads = Vars.active_downloads.copy()
            for link, download in downloads.items():
                print_downloader(download=download, link=link)
            current_nums = len(downloads) * 8
            if current_nums < Vars.clear_nums:
                print(f"\033[{current_nums}A",end="",flush=True)
                print("\033[J",end="",flush=True)
            else:
                print(f"{magic_char * current_nums}", end="", flush=True)
                sleep(3)
            Vars.clear_nums = current_nums
        if len(Vars.urls) == 0 and len(Vars.active_downloads) == 0:
            break


def start_downloader():
    os.system("clear")
    print(f"{cBold}{cMagenta}{pyfiglet.figlet_format('Downloader')}{cEnd}")
    Vars.urls = input(f"{cBold}{cBlue}Download links: {cEnd}").split(" ")
    remove_duplicate_links()
    thread = threading.Thread(target=show_downloader)
    thread.start()
    while len(Vars.urls) != 0:
        if len(Vars.active_downloads) < Vars.limit:
            link = Vars.urls[0]
            download = add_download_link(link)
            if download is not None:
                Vars.active_downloads.update({link: download})
            else:
                Vars.failed_downloads.append(link)
            Vars.urls.pop(0)
    thread.join()
    show_post_download_stats()


if __name__ == "__main__":
    try:
        start_downloader()
    except KeyboardInterrupt:
        aria2.remove_all(force=True)
        print(f"\033[{Vars.clear_nums}B", end="", flush=True)
    finally:
        print(show_cursor, end="")
