import aria2p
from pgrep import pgrep
import subprocess

from rich.console import Console

# Start Aria Daemon
ariaPidLen = len(pgrep("aria2"))

if ariaPidLen == 0:
    subprocess.call(["bash", "/home/athul/Documents/DownloadManager/aria.sh"])

# Console color
console = Console()

# Start Aria Client
aria2 = aria2p.API(aria2p.Client(host="http://localhost", port=6800, secret=""))
