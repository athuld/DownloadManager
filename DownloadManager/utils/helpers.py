import codecs
import os
import subprocess
from pathlib import Path

import pyfiglet

from DownloadManager import aria2
from DownloadManager.vars import Vars
from DownloadManager.utils.colors import cGreen, cBold, cRed, cEnd, cMagenta


# remove duplicate links
def remove_duplicate_links():
    cleaned_urls = list(set(Vars.urls))
    Vars.urls = cleaned_urls.copy()
    Vars.urls_cpy = Vars.urls.copy()


# Get File-type
def getFileType(fileName):
    _, file_ex = os.path.splitext(fileName)
    audio_formats = {".aac", ".flac", ".m4a", ".mp3", ".opus", ".vorbis", ".wav"}
    videoFormats = {".mp4", ".mov", ".wmv", ".flv", ".avi", ".avchd", ".mkv", ".webm"}
    compressFormats = {".zip", ".tar", ".rar", ".7z", ".gz"}

    if file_ex in audio_formats:
        dict = {"type": "Audio File", "moveFolder": "Audios"}
    elif file_ex in videoFormats:
        dict = {"type": "Video File", "moveFolder": "Videos"}
    elif file_ex in compressFormats:
        dict = {"type": "Compressed File", "moveFolder": "Compressed"}
    else:
        dict = {"type": "Other File", "moveFolder": "Others"}

    return dict


# Progress Bar
def getProgress(cmpBytes, totalBytes):
    completed = cmpBytes / 8
    total = totalBytes / 8
    p = 0 if total == 0 else round(completed * 100 / total)
    p = min(max(p, 0), 100)
    cFull = p * 4 // 8
    p_str = "▓" * cFull
    p_str += "░" * (50 - cFull)
    p_str = f"{cBold}{cRed}[{cGreen}{p_str}{cEnd}{cBold}{cRed}]{cEnd}"
    return p_str


# Generate GID
def generate_gid():
    gid = codecs.encode(os.urandom(8), "hex").decode()
    return gid


# post download actions
def post_download_action(file_details_list, download, link):
    fileInfo = file_details_list["fileInfo"]
    moveFolder = fileInfo["moveFolder"]
    if download.has_failed:
        Vars.failed_downloads.append(link)
        print(f"\n{cRed}Error Occured in download{cEnd}")
        subprocess.Popen(
            ["notify-send", "Dowload Failed", f"--icon={Vars.imgDir}/failed.png"]
        )
    else:
        downFile = Path(f"{Vars.downDir}/{moveFolder}/{download.name}")
        if downFile.exists():
            os.remove(downFile)
        aria2.move_files([download], f"{Vars.downDir}/{moveFolder}/", True)
        Vars.finished_downloads.append(file_details_list)
        subprocess.Popen(
            [
                "notify-send",
                "Dowload Completed",
                f"{download.name}",
                f"--icon={Vars.imgDir}/success.png",
            ]
        )
    del Vars.active_downloads[link]


# show finished/failed downloads
def show_post_download_stats():
    os.system("clear")
    print(f"{cBold}{cMagenta}{pyfiglet.figlet_format('Downloader')}{cEnd}")
    finished_nums = len(Vars.finished_downloads)
    if finished_nums > 0:
        print(
            f"\n{cBold}{cGreen} Finished downloading {finished_nums} links successfully!{cEnd}"
        )

    for download in Vars.finished_downloads:
        fileInfo = download["fileInfo"]
        moveFolder = fileInfo["moveFolder"]
        fileName = download["fileName"]
        fileType = download["fileType"]
        totalString = download["totalString"]
        print(
            f"\n{cBold} Filename: {fileName}\n{cBold} Size: {totalString}\n{cBold} Type:{cEnd} {fileType}\n{cBold} Path:{cEnd} {cBold}{cMagenta}{Vars.downDir}/{moveFolder}{cEnd}"
        )
    failed_nums = len(Vars.failed_downloads)
    if failed_nums > 0:
        print(f"\n{cBold}--------------------------------------------------{cEnd}")
        print(f"\n{cBold}{cRed} Failed to download {failed_nums} links{cEnd}")
        for link in Vars.failed_downloads:
            print(f"\n{cBold} {link}{cEnd}")
