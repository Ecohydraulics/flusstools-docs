"""
Description
"""

import os, sys
sys.path.insert(0, os.path.abspath("."))
from helpers import *


logger = logging.getLogger(__name__)


def browse(root, entry, select='file', ftypes=[('All files', '*')]):
    """GUI button command opens browser window and adds selected file/folder to entry"""
    if select == 'file':
        filename = filedialog.askopenfilename(parent=root, title='Choose a file', filetypes=ftypes)
        if filename:
            entry.delete(0, tk.END)
            entry.insert(tk.END, filename)

    elif select == 'files':
        files = filedialog.askopenfilenames(parent=root, title='Choose files', filetypes=ftypes)
        l = root.tk.splitlist(files)
        entry.delete(0, tk.END)
        entry.insert(tk.END, l)

    elif select == 'folder':
        dirname = filedialog.askdirectory(parent=root, initialdir=entry.get(), title='Choose a directory')
        if len(dirname) > 0:
            entry.delete(0, tk.END)
            entry.insert(tk.END, dirname + '/')


def check_use(filepath):
    """Checks if a file or list of files is in use by another process.
    If the file cannot be opened or there is an associated .lock file, it throws an exception.
    """

    if type(filepath) == list:
        for f in filepath:
            check_use(f)
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
                        logger.error('%s is open in another program. Close the file and try again.' % filepath)
                        raise Exception('%s is open in another program. Close the file and try again.' % filepath)

        except IOError:
            logger.error('%s is open in another program. Close the file and try again.' % filepath)
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
            logger.info(e)
            messagebox.showerror('Error', e)
    return wrapper


def get_all_files(dir, prefix='', suffix='', nesting=True):
    """
    Returns list of all files in directory

    Args:
        dir (str): the directory of interest
        prefix (str): if provided, files returned must start with this
        suffix (str): if provided, files returned must end with this
        nesting (bool): if True, looks in all subdirectories of dir. If false, only looks at top-level.
    """
    l = []
    for path, subdirs, files in os.walk(dir):
        for name in files:
            if name.startswith(prefix) and name.endswith(suffix) and (nesting or (path == dir)):
                l.append(os.path.join(path, name))
    return l


def get_largest(directory):
    """returns name of largest file in directory"""
    largest_so_far = 0
    filename = ''
    for name in os.listdir(directory):
        size = os.path.getsize(os.path.join(directory, name))
        if size > largest_so_far:
            largest_so_far = size
            filename = name

    return os.path.join(directory, filename)


def init_logger(filename):
    """Initializes logger"""
    logging.basicConfig(filename=os.path.basename(filename).replace('.py', '.log'), filemode='w', level=logging.INFO)
    stderrLogger = logging.StreamHandler()
    stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
    logging.getLogger().addHandler(stderrLogger)
    return


def las_files(directory):
    """returns list of all .las/.laz files in directory (at top level)"""
    l = []
    for name in os.listdir(directory):
        if name.endswith('.las') or name.endswith('.laz'):
            l.append(directory + name)

    return l


def split_list(l, break_pts):
    """returns list l split up into sublists at break point indices"""
    l_0 = len(l)
    sl = []
    if break_pts is []:
        return [l]
    else:
        for brk in break_pts:
            delta_l = l_0 - len(l)
            sl.append(l[:brk - delta_l])
            l = l[brk - delta_l:]
        sl.append(l)
    return sl


def split_reaches(l, new_reach_pts):
    """splits l into sections where new_reach_pts contains the starting indices for each slice"""
    new_reach_pts = sorted(new_reach_pts)
    sl = [l[i1:i2] for i1, i2 in zip(new_reach_pts, new_reach_pts[1:])]
    last_index = new_reach_pts[-1]
    sl.append(l[last_index:])
    return sl
