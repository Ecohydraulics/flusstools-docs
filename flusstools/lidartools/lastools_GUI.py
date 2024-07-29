"""
Main script to run lidar processing through the GUI
"""

from .lastools_core import *


def create_gui():
    # make the GUI window
    root = tk.Tk()
    root.wm_title('LiDAR Reprocessing App (based on LAStools)')

    # specify relevant directories/files

    L1 = tk.Label(root, text='LAStools /bin/ directory:')
    L1.grid(sticky=tk.E, row=0, column=1)
    E1 = tk.Entry(root, bd=5)
    E1.insert(tk.END, 'C:\\LAStools\\bin\\')
    E1.grid(row=0, column=2)
    b1 = tk.Button(root, text='Browse', command=lambda: browse(root, E1, select='folder'))
    b1.grid(sticky=tk.W, row=0, column=3)

    L2 = tk.Label(root, text='LiDAR data directory:')
    L2.grid(sticky=tk.E, row=1, column=1)
    E2 = tk.Entry(root, bd=5)
    E2.insert(tk.END, sys.path[0])
    E2.grid(row=1, column=2)
    b2 = tk.Button(root, text='Browse', command=lambda: browse(root, E2, select='folder'))
    b2.grid(sticky=tk.W, row=1, column=3)

    L3 = tk.Label(root, text='Ground area .shp file (optional):')
    shp_var = tk.StringVar()
    L3.grid(sticky=tk.E, row=2, column=1)
    E3 = tk.Entry(root, bd=5, textvariable=shp_var)
    E3.grid(row=2, column=2)
    b3 = tk.Button(root, text='Browse', command=lambda: browse(root, E3, select='file', ftypes=[('Shapefile', '*.shp'),
                                                                                                ('All files', '*')]
                                                               )
                   )
    b3.grid(sticky=tk.W, row=2, column=3)

    # if no ground shapefile is provided, disable the fine setting and just run on "coarse"
    def trace_choice(*args):
        if shp_var.get() == '':
            for widget in [E1b, E2b, E3b, E4b, E5b]:
                widget.config(state=tk.DISABLED)
        else:
            for widget in [E1b, E2b, E3b, E4b, E5b]:
                widget.config(state='normal')

    shp_var.trace('w', trace_choice)

    # specify lasground_new parameters
    root.grid_rowconfigure(5, minsize=80)

    LC1 = tk.Label(root, text='standard/coarse classification parameters:')
    LC1.grid(row=5, column=0, columnspan=2)

    L1a = tk.Label(root, text='step size:')
    L1a.grid(sticky=tk.E, row=6)
    E1a = tk.Entry(root, bd=5)
    E1a.grid(row=6, column=1)

    L2a = tk.Label(root, text='bulge:')
    L2a.grid(sticky=tk.E, row=7)
    E2a = tk.Entry(root, bd=5)
    E2a.grid(row=7, column=1)

    L3a = tk.Label(root, text='spike:')
    L3a.grid(sticky=tk.E, row=8)
    E3a = tk.Entry(root, bd=5)
    E3a.grid(row=8, column=1)

    L4a = tk.Label(root, text='down spike:')
    L4a.grid(sticky=tk.E, row=9)
    E4a = tk.Entry(root, bd=5)
    E4a.grid(row=9, column=1)

    L5a = tk.Label(root, text='offset:')
    L5a.grid(sticky=tk.E, row=10)
    E5a = tk.Entry(root, bd=5)
    E5a.grid(row=10, column=1)

    LC2 = tk.Label(root, text='fine classification parameters (in ground area):')
    LC2.grid(row=5, column=2, columnspan=2)

    L1b = tk.Label(root, text='step size:')
    L1b.grid(sticky=tk.E, row=6, column=2)
    E1b = tk.Entry(root, bd=5, state=tk.DISABLED)
    E1b.grid(row=6, column=3)

    L2b = tk.Label(root, text='bulge:')
    L2b.grid(sticky=tk.E, row=7, column=2)
    E2b = tk.Entry(root, bd=5, state=tk.DISABLED)
    E2b.grid(row=7, column=3)

    L3b = tk.Label(root, text='spike:')
    L3b.grid(sticky=tk.E, row=8, column=2)
    E3b = tk.Entry(root, bd=5, state=tk.DISABLED)
    E3b.grid(row=8, column=3)

    L4b = tk.Label(root, text='down spike:')
    L4b.grid(sticky=tk.E, row=9, column=2)
    E4b = tk.Entry(root, bd=5, state=tk.DISABLED)
    E4b.grid(row=9, column=3)

    L5b = tk.Label(root, text='offset:')
    L5b.grid(sticky=tk.E, row=10, column=2)
    E5b = tk.Entry(root, bd=5, state=tk.DISABLED)
    E5b.grid(row=10, column=3)

    # specify units
    L5 = tk.Label(root, text='Units')
    L5.grid(sticky=tk.W, row=11, column=2)
    root.grid_rowconfigure(11, minsize=80)
    unit_var = tk.StringVar()
    R5m = tk.Radiobutton(root, text='Meters', variable=unit_var, value=' ')
    R5m.grid(sticky=tk.E, row=12, column=1)
    R5f = tk.Radiobutton(root, text='US Feet', variable=unit_var, value=' -feet -elevation_feet ')
    R5f.grid(row=12, column=2)
    unit_var.set(' ')

    # specify number of cores
    L4 = tk.Label(root, text='Number of cores for processing')
    L4.grid(sticky=tk.E, row=13, column=1, columnspan=2)
    root.grid_rowconfigure(13, minsize=80)
    core_num = tk.IntVar()
    R1 = tk.Radiobutton(root, text='1', variable=core_num, value=1)
    R1.grid(sticky=tk.E, row=14, column=1)
    R2 = tk.Radiobutton(root, text='2', variable=core_num, value=2)
    R2.grid(row=14, column=2)
    R4 = tk.Radiobutton(root, text='4', variable=core_num, value=4)
    R4.grid(sticky=tk.W, row=14, column=3)
    R8 = tk.Radiobutton(root, text='8', variable=core_num, value=8)
    R8.grid(sticky=tk.E, row=15, column=1)
    R16 = tk.Radiobutton(root, text='16', variable=core_num, value=16)
    R16.grid(row=15, column=2)
    R32 = tk.Radiobutton(root, text='32', variable=core_num, value=32)
    R32.grid(sticky=tk.W, row=15, column=3)
    core_num.set(16)

    L5 = tk.Label(root, text='Keep original ground/veg points: ')
    L5.grid(sticky=tk.E, row=16, column=1)
    keep_originals = tk.BooleanVar()
    C1 = tk.Checkbutton(root, variable=keep_originals)
    C1.grid(sticky=tk.W, row=16, column=2)
    keep_originals.set(True)

    # make 'Run' button in GUI to call the process_lidar() function
    b = tk.Button(root, text='  Run   ',
                  command=lambda: process_lidar(lastoolsdir=E1.get(),
                                                lidardir=E2.get(),
                                                ground_poly=E3.get(),
                                                cores=core_num.get(),
                                                units_code=unit_var.get()[1:-1],
                                                keep_orig_pts=keep_originals.get(),
                                                coarse_step=E1a.get(),
                                                coarse_bulge=E2a.get(),
                                                coarse_spike=E3a.get(),
                                                coarse_down_spike=E4a.get(),
                                                coarse_offset=E5a.get(),
                                                fine_step=E1b.get(),
                                                fine_bulge=E2b.get(),
                                                fine_spike=E3b.get(),
                                                fine_down_spike=E4b.get(),
                                                fine_offset=E5b.get()
                                                )
                  )

    b.grid(sticky=tk.W, row=17, column=2)
    root.grid_rowconfigure(17, minsize=80)

    root.mainloop()


if __name__ == '__main__':
    # launch GUI
    create_gui()
