from pathlib import Path
import aria2p
import time
from rich.console import Console
import pyfiglet
import os
from pgrep import pgrep
import subprocess

# Start Aria Daemon
ariaPidLen = len(pgrep("aria2"))

if ariaPidLen == 0:
    subprocess.call(["bash", "/home/athul/Documents/DownloadManager/aria.sh"])

# Start Aria Client
aria2 = aria2p.API(aria2p.Client(host="http://localhost", port=6800, secret=""))

console = Console()

# Colors
cMagenta = "\033[95m"
cBlue = "\033[94m"
cCyan = "\033[96m"
cGreen = "\033[92m"
cYellow = "\033[93m"
cRed = "\033[91m"
cEnd = "\033[0m"
cBold = "\033[1m"

# Default Download directory
DOWN = "/home/athul/Downloads"

# Image directory
imgDir = "/home/athul/.imgs"


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


# Sort Files
def getFileType(fileName):
    _, file_ex = os.path.splitext(fileName)
    audioFormats = {".aac", ".flac", ".m4a", ".mp3", ".opus", ".vorbis", ".wav"}
    videoFormats = {".mp4", ".mov", ".wmv", ".flv", ".avi", ".avchd", ".mkv", ".webm"}
    compressFormats = {".zip", ".tar", ".rar", ".7z", ".gz"}

    if file_ex in audioFormats:
        dict = {"type": "Audio File", "moveFolder": "Audios"}
    elif file_ex in videoFormats:
        dict = {"type": "Video File", "moveFolder": "Videos"}
    elif file_ex in compressFormats:
        dict = {"type": "Compressed File", "moveFolder": "Compressed"}
    else:
        dict = {"type": "Other File", "moveFolder": "Others"}

    return dict


os.system("clear")
print(f"{cBold}{cMagenta}{pyfiglet.figlet_format('Downloader')}{cEnd}")

urls = input(f"{cBold}{cBlue}Download links: {cEnd}").split(" ")

for link in urls:
    aria2.purge()
    aria2.add(link)
    with console.status("[bold green]Checking download link...") as status:
        while True:
            downloads = aria2.get_downloads()
            if downloads[0].gid != None and downloads[0].total_length != 0:
                break

    fileInfo = getFileType(downloads[0].name)
    magic_char = "\033[F"
    fileName = f"{cYellow}{downloads[0].name}{cEnd}"
    fileType = f"{cBold}{cYellow}{fileInfo['type']}{cEnd}"
    totalString = f"{cBold}{cBlue}{downloads[0].total_length_string(True)}{cEnd}"
    print(f"\n\n{cBold}{cMagenta} Downloading [ {urls.index(link)+1} / {len(urls)} ] links{cEnd}")
    print(f"{cBold} Filename:{cEnd} {fileName}\n\n\n")

    while downloads[0].is_complete != True:
        try:
            downloads[0].update()
            cmpBytes = downloads[0].completed_length_string(False).split(" ")
            progressPerc = f"{cBold}{cCyan}{downloads[0].progress_string()}{cEnd}"
            speedString = (
                f"{cBold}{cMagenta}{downloads[0].download_speed_string(True)}{cEnd}"
            )
            cmpString = (
                f"{cBold}{cBlue}{downloads[0].completed_length_string(True)}{cEnd}"
            )
            etaString = f"{cBold}{cBlue}{downloads[0].eta_string(1)}{cEnd}"
            progressBar = getProgress(int(cmpBytes[0]), downloads[0].total_length)
            print(
                f"{magic_char*3}{cBold} Progress:{cEnd}{progressBar} {progressPerc}\n{cBold} Downloaded:{cEnd} {cmpString} {cBold}of{cEnd} {totalString}\n{cBold} Speed:{cEnd} {speedString} {cBold} ETA:{cEnd} {etaString}\n{cBold} Type:{cEnd} {fileType}",
                end="",
                flush=True,
            )

            time.sleep(1)
        except KeyboardInterrupt:
            aria2.remove_all(True)
            subprocess.Popen(
                ["notify-send", "Dowload Failed", f"--icon={imgDir}/failed.png"]
            )
        except Exception:
            subprocess.Popen(
                ["notify-send", "Dowload Failed", f"--icon={imgDir}/failed.png"]
            )

    moveFolder = fileInfo["moveFolder"]
    if downloads[0].has_failed:
        print(f"\n{cRed}Error Occured in download{cEnd}")
        subprocess.Popen(
            ["notify-send", "Dowload Failed", f"--icon={imgDir}/failed.png"]
        )
    else:
        downFile = Path(f"{DOWN}/{moveFolder}/{downloads[0].name}")
        if downFile.exists():
            os.remove(downFile)
        aria2.move_files(downloads, f"{DOWN}/{moveFolder}/", True)
        os.system("clear")
        print(f"{cBold}{cMagenta}{pyfiglet.figlet_format('Downloader')}{cEnd}")
        print(
            f"\n {cBold}{cGreen}File Downloaded Successfully!\n{cEnd}{cBold} Filename: {fileName}\n{cBold} Size: {totalString}\n{cBold} Type:{cEnd} {fileType}\n{cBold} Path:{cEnd} {cBold}{cMagenta}{DOWN}/{moveFolder}{cEnd}"
        )
        subprocess.Popen(
            [
                "notify-send",
                "Dowload Completed",
                f"{downloads[0].name}",
                f"--icon={imgDir}/success.png",
            ]
        )
