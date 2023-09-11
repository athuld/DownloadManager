import os


HOME=os.path.expanduser("~")

class Vars(object):
    # Active downloads dict
    active_downloads = {}
    # Finished downloads list
    finished_downloads = []
    # Failed downloads list
    failed_downloads = []
    # Original urls from user
    urls = []
    # Copy of original urls from user
    urls_cpy = []
    # Var used for clear lines
    clear_nums=1
    # Limit of the parallel downloads
    limit=3
    # Default Download directory
    downDir = f"{HOME}/Downloads"
    # Image directory
    imgDir = f"{os.getcwd()}/imgs"
