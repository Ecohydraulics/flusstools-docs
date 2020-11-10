"""Global variables"""
from var_config import *


def cache(fun):
    """Makes a function running in a temoprary ``__cache__`` sub-folder to enable deleting temporary trash files."""
    def wrapper(*args, **kwargs):
        check_cache()
        fun(*args, **kwargs)
        remove_directory(cache_folder)
    wrapper.__doc__ = fun.__doc__
    return wrapper


def check_cache():
    """Creates the cache folder if it does not exist."""
    try:
        os.makedirs(cache_folder)
    except OSError:
        pass


def remove_directory(directory):
    """Removes a directory and all its contents - be careful!

    Args:
        directory (str): directory to remove (delete)

    Returns:
        None: Deletes directory.
    """
    try:
        for root, dirs, files in os.walk(directory):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        shutil.rmtree(directory)
    except PermissionError:
        print("WARNING: Could not remove %s (files locked by other program)." % directory)
    except FileNotFoundError:
        print("WARNING: The directory %s does not exist." % directory)
    except NotADirectoryError:
        print("WARNING: %s is not a directory." % directory)
