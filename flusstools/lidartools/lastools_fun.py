"""
Description
"""


from fuzzycorr import *


def browse(root, entry, select='file', ftypes=[('All files', '*')]):
    """GUI button command opens browser window and adds selected file/folder to entry"""
    if select == 'file':
        filename = filedialog.askopenfilename(
            parent=root, title='Choose a file', filetypes=ftypes)
        if filename:
            entry.delete(0, tk.END)
            entry.insert(tk.END, filename)

    elif select == 'files':
        files = filedialog.askopenfilenames(
            parent=root, title='Choose files', filetypes=ftypes)
        l = root.tk.splitlist(files)
        entry.delete(0, tk.END)
        entry.insert(tk.END, l)

    elif select == 'folder':
        dirname = filedialog.askdirectory(
            parent=root, initialdir=entry.get(), title='Choose a directory')
        if len(dirname) > 0:
            entry.delete(0, tk.END)
            entry.insert(tk.END, dirname + '/')


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


def get_las_files(directory):
    """returns list of all .las/.laz files in directory (at top level)"""
    l = []
    for name in os.listdir(directory):
        if name.endswith('.las') or name.endswith('.laz'):
            l.append(directory + name)
    return l


def split_list(list2split, break_pts):
    """returns list l split up into sublists at break point indices"""
    act_len = len(list2split)
    sub_list = []
    if break_pts is []:
        return [list2split]
    else:
        for brk in break_pts:
            delta_l = act_len - len(list2split)
            sub_list.append(list2split[:brk - delta_l])
            list2split = list2split[brk - delta_l:]
        sub_list.append(list2split)
    return sub_list


def split_reaches(list_of_reaches, new_reach_pts):
    """splits l into sections where new_reach_pts contains the starting indices for each slice"""
    new_reach_pts = sorted(new_reach_pts)
    sub_list = [list_of_reaches[i1:i2]
                for i1, i2 in zip(new_reach_pts, new_reach_pts[1:])]
    last_index = new_reach_pts[-1]
    sub_list.append(list_of_reaches[last_index:])
    return sub_list
