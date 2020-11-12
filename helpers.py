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


def check_if_file_in_use(filepath):
    """Checks if a file or list of files is in use by another process.
    If the file cannot be opened or there is an associated .lock file, it throws an exception.
    """

    if type(filepath) == list:
        for f in filepath:
            check_if_file_in_use(f)
        return

    file_object = None
    if os.path.exists(filepath):
        try:
            buffer_size = 8
            # Opening file in append mode and read the first 8 characters.
            file_object = open(filepath, 'a', buffer_size)
            if file_object:
                for filename in os.listdir(os.path.dirname(filepath)):
                    if filename.startswith(os.path.basename(filepath)) and filename.endswith('.lock'):
                        logging.error('%s is open in another program. Close the file and try again.' % filepath)
                        raise Exception('%s is open in another program. Close the file and try again.' % filepath)

        except IOError:
            logging.error('%s is open in another program. Close the file and try again.' % filepath)
            raise Exception('%s is open in another program. Close the file and try again.' % filepath)

        finally:
            if file_object:
                file_object.close()
    return


# wrapper to show error message when a command fails
def err_info(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logging.info(e)
            messagebox.showerror('Error', e)
    return wrapper


def get_file_names(directory, prefix='', suffix='', nesting=True):
    """
    Returns list of all files in directory

    Args:
        directory (str): the directory of interest
        prefix (str): if provided, files returned must start with this
        suffix (str): if provided, files returned must end with this
        nesting (bool): if True, looks in all subdirectories of dir. If false, only looks at top-level.
    """
    l = []
    for path, subdirs, files in os.walk(directory):
        for name in files:
            if name.startswith(prefix) and name.endswith(suffix) and (nesting or (path == directory)):
                l.append(os.path.join(path, name))
    return l


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
