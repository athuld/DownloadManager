import aria2p
import os
import subprocess

from rich.console import Console

# Start Aria Daemon
subprocess.call(["bash", f"{os.getcwd()}/aria.sh"])

# Console color
console = Console()

# Start Aria Client
aria2 = aria2p.API(aria2p.Client(host="http://localhost", port=6800, secret=""))
