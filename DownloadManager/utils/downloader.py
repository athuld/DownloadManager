import subprocess
import time
import sys

from aria2p.downloads import Download

from DownloadManager import aria2, console
from DownloadManager.vars import Vars
from DownloadManager.utils.colors import (
    cYellow,
    cEnd,
    cBold,
    cBlue,
    cMagenta,
    cCyan,
    hide_cursor,
)

from DownloadManager.utils.helpers import (
    generate_gid,
    getFileType,
    getProgress,
    post_download_action,
)


def add_download_link(link):
    gid = generate_gid()
    opts = {"gid": gid,"dir":"/tmp/downloads"}
    timeout = time.time() + 15
    aria2.add(uri=link, options=opts)
    with console.status("[bold green]Checking download link...") as status:
        while True:
            download = aria2.get_download(gid=gid)
            if time.time() > timeout:
                aria2.remove(downloads=[download])
                return None
            if download.total_length != 0:
                break

    return download


def print_downloader(download: Download, link):
    fileInfo = getFileType(download.name)
    fileName = f"{cYellow}{download.name}{cEnd}"
    fileType = f"{cBold}{cYellow}{fileInfo['type']}{cEnd}"
    totalString = f"{cBold}{cBlue}{download.total_length_string(True)}{cEnd}"
    file_details_list = {
        "fileInfo": fileInfo,
        "fileName": fileName,
        "fileType": fileType,
        "totalString": totalString,
    }
    print(
        f"\n\n{cBold}{cMagenta} Downloading [ {Vars.urls_cpy.index(link) + 1} / {len(Vars.urls_cpy)} ] links{cEnd}"
    )
    print(f"{cBold} Filename:{cEnd} {fileName}")

    if not download.is_complete:
        try:
            download.update()
            cmpBytes = download.completed_length_string(False).split(" ")
            progressPerc = f"{cBold}{cCyan}{download.progress_string()}{cEnd}"
            speedString = (
                f"{cBold}{cMagenta}{download.download_speed_string(True)}{cEnd}"
            )
            cmpString = f"{cBold}{cBlue}{download.completed_length_string(True)}{cEnd}"
            etaString = f"{cBold}{cBlue}{download.eta_string(1)}{cEnd}"
            progressBar = getProgress(int(cmpBytes[0]), download.total_length)
            print(
                f"{hide_cursor}{cBold} Progress:{cEnd}{progressBar} {progressPerc}\n{cBold} Downloaded:{cEnd} {cmpString} {cBold}of{cEnd} {totalString}\n{cBold} Speed:{cEnd} {speedString} {cBold} ETA:{cEnd} {etaString}\n{cBold} Type:{cEnd} {fileType}"
            )
        except KeyboardInterrupt:
            aria2.remove_all(True)
            subprocess.Popen(
                ["notify-send", "Download Failed", f"--icon={Vars.imgDir}/failed.png"]
            )
        except Exception:
            subprocess.Popen(
                ["notify-send", "Download Failed", f"--icon={Vars.imgDir}/failed.png"]
            )
    if download.is_complete or download.has_failed:
        post_download_action(file_details_list, download, link)
