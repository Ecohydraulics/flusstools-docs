"""
Things to consider adding:
    choice of las or laz output
    set default values for lasground_new params
    clip structures step
    lasclassify params to identify buildings
    use veg polygon (if given) instead of inverse ground polygon to clip veg points
"""

from .lastools_fun import *


class DF(pd.DataFrame):
    """Extended pandas DataFrame class with an additional title attribute"""

    def __init__(self, data=None, index=None, columns=None, dtype=None, copy=False, title=None):
        pd.DataFrame.__init__(self, data, index, columns, dtype, copy)
        self.title = title

    def show(self):
        if self.title:
            print(self.title)


def ar1_acorr(series, maxlags=''):
    """Returns lag, autocorrelation, and confidence interval using geometric autocorrelation for AR1 fit of series"""
    n = len(series)
    if maxlags == '':
        maxlags = int(n/2)
    # use phi as lag-1 correlation of data
    phi = np.corrcoef(series[:-1], series[1:])[0][1]
    lags = range(maxlags+1)
    acorrs = [phi**k for k in lags]
    lower_band, upper_band = zip(*[r_confidence_interval(phi**k, n - k) for k in lags])

    return lags, acorrs, lower_band, upper_band


def cmd(command):
    """Executes command prompt command"""
    try:
        res = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        msg = 'Command failed: %s' % command
        logging.error(msg)
        raise Exception(msg)

    msg = str(res.communicate()[1])
    # if using for LAStools, get rid of the annoying LAStools licensing message.
    msg = msg.replace(msg_from_lastools, '')
    logging.info(msg)
    return


def cox_acorr(series, maxlags=''):
    """
    :param series: (list)
    :param maxlags: (str)
    :return: two lists (lags and autocorrelation), using Cox variant 3 of ACF
    """
    n = len(series)
    if maxlags == '':
        maxlags = int(n/2)
    xbar = np.mean(series)
    lags = range(maxlags+1)
    acorrs = []
    for k in lags:
        if k == 0:
            acorrs.append(1)
        else:
            s1 = series[:-k]
            s2 = series[k:]
            numerator = 1.0/(n - k) * sum([(x1 - xbar) * (x2 - xbar) for x1, x2 in zip(s1, s2)])
            denominator = 1.0/n * sum([(xi - xbar)**2 for xi in series])
            acorrs.append(numerator*1.0/denominator)

    return lags, acorrs


def ft(x, y):
    """Returns the fourier transform magnitude of the x,y data"""
    n = len(x)
    spacing = abs(x[1]-x[0])
    xf = np.linspace(0, 1/(2.0*spacing), n//2)
    yf = np.fft.fft(y)
    yf = list(map(lambda k: 2.0/n*np.abs(k), yf))[:n//2]
    return xf, yf


# input working directory for LAStools and directory containing .las/.laz files
# creates a .txt file for LAStools containing list of .las/.laz file names
# returns the name of the .txt file.
def lof_text(pwd, src):
    """creates a .txt file in pwd (LAStools bin) containing a list of .las/.laz filenames from src directory"""
    filename = pwd + 'file_list.txt'
    f = open(filename, 'w+')

    if type(src) == str:
        for i in get_las_files(src):
            f.write('%s\n' % i)
    else:
        # this is the case when there are multiple source folders
        for i in [name for source in src for name in get_las_files(source)]:
            f.write('%s\n' % i)
    f.close()
    return filename


# input .las/.laz filename, outputs point density (after running lasinfo)
def pd(filename):
    """returns point density from lasinfo output .txt file"""
    # name of txt output file from lasinfo
    filename = filename[:-4] + '.txt'
    f = open(filename, 'r')
    text = f.readlines()
    for line in text:
        if line.startswith('point density:'):
            d = line.split(' ')
            d = d[d.index('returns') + 1]
            return float(d)


# the main function that runs when 'run' button is clicked
@err_info
def process_lidar(lastoolsdir,
                  lidardir,
                  ground_poly,
                  cores,
                  units_code,
                  keep_orig_pts,
                  coarse_step,
                  coarse_bulge,
                  coarse_spike,
                  coarse_down_spike,
                  coarse_offset,
                  fine_step,
                  fine_bulge,
                  fine_spike,
                  fine_down_spike,
                  fine_offset
                  ):
    """Executes main LAStools processing workflow. See readme for more info."""

    classes = ['01-Default',
               '02-Ground',
               '05-Vegetation',
               '06-Building'
               ]

    if (ground_poly != '') and (keep_orig_pts == True):
        # run on coarse and fine settings, need to clip and remove duplicates after merging
        outdirs = ['00_separated',
                   '00_declassified',
                   '01_tiled',
                   '02a_lasground_new_coarse',
                   '02b_lasground_new_fine',
                   '03a_lasheight_coarse',
                   '03b_lasheight_fine',
                   '04a_lasclassify_coarse',
                   '04b_lasclassify_fine',
                   '05a_lastile_rm_buffer_coarse',
                   '05b_lastile_rm_buffer_fine',
                   '06a_separated_coarse',
                   '06b_separated_fine',
                   '07a_ground_clipped_coarse',
                   '07b_ground_clipped_fine',
                   '08_ground_merged',
                   '09_ground_rm_duplicates',
                   '10_veg_new_merged',
                   '11_veg_new_clipped',
                   '12_veg_merged',
                   '13_veg_rm_duplicates'
                   ]

    elif (ground_poly == '') and keep_orig_pts:
        # only classify with coarse settings, no clipping, but need to remove duplicates
        outdirs = ['00_separated',
                   '00_declassified',
                   '01_tiled',
                   '02_lasground_new',
                   '03_lasheight',
                   '04_lasclassify',
                   '05_lastile_rm_buffer',
                   '06_separated',
                   '08_ground_merged',
                   '09_ground_rm_duplicates',
                   '12_veg_merged',
                   '13_veg_rm_duplicates'
                   ]

    elif (ground_poly == '') and not keep_orig_pts:
        # only classify with coarse setting, no clipping or removing duplicates necessary
        outdirs = ['00_separated',
                   '00_declassified',
                   '01_tiled',
                   '02_lasground_new',
                   '03_lasheight',
                   '04_lasclassify',
                   '05_lastile_rm_buffer',
                   '06_separated'
                   ]

    elif (ground_poly != '') and not keep_orig_pts:
        # run on coarse and fine settings, clip, but no removing duplicates needed
        outdirs = ['00_separated',
                   '00_declassified',
                   '01_tiled',
                   '02a_lasground_new_coarse',
                   '02b_lasground_new_fine',
                   '03a_lasheight_coarse',
                   '03b_lasheight_fine',
                   '04a_lasclassify_coarse',
                   '04b_lasclassify_fine',
                   '05a_lastile_rm_buffer_coarse',
                   '05b_lastile_rm_buffer_fine',
                   '06a_separated_coarse',
                   '06b_separated_fine',
                   '07a_ground_clipped_coarse',
                   '07b_ground_clipped_fine',
                   '08_ground_merged',
                   '10_veg_new_merged',
                   '11_veg_new_clipped',
                   '12_veg_merged'
                   ]

    # make new directories for output from each step in processing
    for outdir in outdirs:
        if os.path.isdir(lidardir + outdir) == False:
            os.mkdir(lidardir + outdir)

    if len(os.listdir(lidardir + outdirs[0])) != 0:
        msg = 'Output directories must initially be empty. Move or delete the data currently in output directories.'
        logging.error(msg)
        raise Exception(msg)

    # in each 'separated' folder, create subdirs for each class type
    if ground_poly != '':
        sepdirs = [lidardir + '00_separated',
                   lidardir + '06a_separated_coarse',
                   lidardir + '06b_separated_fine'
                   ]
    else:
        sepdirs = [lidardir + '00_separated',
                   lidardir + '06_separated'
                   ]
    for sepdir in sepdirs:
        for class_type in classes:
            class_dir = sepdir + '/' + class_type
            if os.path.isdir(class_dir) == False:
                os.mkdir(class_dir)

    logging.info('Created directories for output data')

    # create declassified points
    logging.info('Declassifying copy of original point cloud...')

    # get list of filenames for original LiDAR data (all .las and .laz files in lidardir)
    lidar_files = []
    for path, subdirs, files in os.walk(lidardir):
        for name in files:
            if name.endswith('.las') or name.endswith('.laz'):
                lidar_files.append(path + '/' + name)

    if lidar_files == []:
        msg = 'No .las or .laz files in %s or its subdirectories' % lidardir
        logging.error(msg)
        raise Exception(msg)

    # copy original files into '00_declassified' folder
    for name in lidar_files:
        shutil.copyfile(name, lidardir + '00_declassified/' + os.path.basename(name))

        # make list of files for LASTools to process
    lof = lof_text(lastoolsdir, lidardir + '00_declassified/')
    # call LAStools command to declassify points and get point density
    cmd('%slasinfo.exe -lof %s -set_classification 1 -otxt -cd' % (lastoolsdir, lof))

    logging.info('OK')

    # separate original data by class type
    logging.info('Separating original data by class type...')

    filename = lastoolsdir + 'file_list.txt'
    f = open(filename, 'w+')
    for i in lidar_files:
        f.write('%s\n' % i)
    f.close()
    lof = filename

    for class_type in classes:
        odir = lidardir + '00_separated' + '/' + class_type + '/'
        class_code = int(class_type.split('-')[0])
        cmd('%slas2las.exe -lof %s -cores %i -keep_classification %i -odir %s -olas' % (
            lastoolsdir, lof, cores, class_code, odir))

    logging.info('OK')


    # create tiling (max 1.5M pts per tile)
    logging.info('Creating tiling...')

    # get point density for each .las file
    ds = []
    for filename in get_las_files(lidardir + '00_declassified/'):
        ds.append(pd(filename))
    # use max point density out of all files to determine tile size
    max_d = max(ds)

    # width of square tile so we have max of 1.5M pts per tile (assuming same number of points per tile)
    # throw in another factor of 0.5 to make sure tiles will be small enough, round to nearest 10
    tile_size = round(0.5 * np.sqrt((1.5 * 10 ** 6) / max_d), -1)

    logging.info('Using tile size of %i' % tile_size)

    odir = lidardir + '01_tiled/'

    # call LAStools command to create tiling
    cmd('%slastile.exe -lof %s -cores %i -o tile.las -tile_size %i -buffer 5 -faf -odir %s -olas' % (
        lastoolsdir, lof, cores, tile_size, odir))

    logging.info('OK')

    # check to make sure tiles are small enough
    logging.info('Checking if largest file has < 1.5M pts (to avoid licensing restrictions)...')
    largest_file = get_largest(odir)
    num = pts(largest_file, lastoolsdir)
    if num < 1500000:
        logging.info('Largest file has %i points, tiles small enough.' % num)
    else:
        logging.info('Tile size not small enough. Retrying with a smaller tile size...')
        while num >= 1500000:
            # delete original set of tiles
            folder = odir
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except:
                    logging.warning('Couldn\'nt delete %s' % file_path)
            # redo tiling
            tile_size = int(tile_size * num * 1.0 / 1500000)
            logging.info('Using tile size of %i' % tile_size)

            cmd('%slastile.exe -lof %s -cores %i -o tile.las -tile_size %i -buffer 5 -faf -odir %s -olas' % (
                lastoolsdir, lof, cores, tile_size, odir))
            # recheck largest tile number of points
            logging.info('Checking if largest file has < 1.5M pts (to avoid licensing restrictions)...')
            largest_file = get_largest(odir)
            num = pts(largest_file, lastoolsdir)
            if num >= 1500000:
                logging.info('Tile size not small enough. Retrying with a smaller tile size...')

    logging.info('OK')

    # run lasground_new on coarse and fine settings
    logging.info('Running ground classification on coarse setting...')

    lof = lof_text(lastoolsdir, lidardir + '01_tiled/')

    if ground_poly != '':
        odir = lidardir + '02a_lasground_new_coarse/'
    else:
        odir = lidardir + '02_lasground_new'

    cmd(
        '%slasground_new.exe -lof %s -cores %i %s -step %s -bulge %s -spike %s -down_spike %s -offset %s -hyper_fine -odir %s -olas' % (
            lastoolsdir,
            lof,
            cores,
            units_code,
            coarse_step,
            coarse_bulge,
            coarse_spike,
            coarse_down_spike,
            coarse_offset,
            odir
        )
    )

    logging.info('OK')

    if ground_poly != '':
        logging.info('Running ground classification on fine setting...')

        odir = lidardir + '02b_lasground_new_fine/'

        cmd(
            '%slasground_new.exe -lof %s -cores %i %s -step %s -bulge %s -spike %s -down_spike %s -offset %s -hyper_fine -odir %s -olas' % (
                lastoolsdir,
                lof,
                cores,
                units_code,
                fine_step,
                fine_bulge,
                fine_spike,
                fine_down_spike,
                fine_offset,
                odir
            )
        )

        logging.info('OK')

    # run lasheight on each data set
    logging.info('Measuring height above ground for non-ground points...')

    if ground_poly != '':
        lof = lof_text(lastoolsdir, lidardir + '02a_lasground_new_coarse/')
        odir = lidardir + '03a_lasheight_coarse/'
    else:
        lof = lof_text(lastoolsdir, lidardir + '02_lasground_new/')
        odir = lidardir + '03_lasheight/'

    cmd('%slasheight.exe -lof %s -cores %i -odir %s -olas' % (lastoolsdir, lof, cores, odir))

    if ground_poly != '':
        lof = lof_text(lastoolsdir, lidardir + '02b_lasground_new_fine/')
        odir = lidardir + '03b_lasheight_fine/'

        cmd('%slasheight.exe -lof %s -cores %i -odir %s -olas' % (lastoolsdir, lof, cores, odir))

    logging.info('OK')

    # run lasclassify on each data set
    logging.info('Classifying non-ground points on coarse setting...')

    if ground_poly != '':
        lof = lof_text(lastoolsdir, lidardir + '03a_lasheight_coarse/')
        odir = lidardir + '04a_lasclassify_coarse/'
    else:
        lof = lof_text(lastoolsdir, lidardir + '03_lasheight/')
        odir = lidardir + '04_lasclassify/'

    cmd('%slasclassify.exe -lof %s -cores %i %s -odir %s -olas' % (lastoolsdir, lof, cores, units_code, odir))

    logging.info('OK')

    if ground_poly != '':
        logging.info('Classifying non-ground points on fine setting...')

        lof = lof_text(lastoolsdir, lidardir + '03b_lasheight_fine/')
        odir = lidardir + '04b_lasclassify_fine/'

        cmd('%slasclassify.exe -lof %s -cores %i %s -odir %s -olas' % (lastoolsdir, lof, cores, units_code, odir))

        logging.info('OK')

    # remove tile buffers on each data set
    logging.info('Removing tile buffers...')
    if ground_poly != '':
        lof = lof_text(lastoolsdir, lidardir + '04a_lasclassify_coarse/')
        odir = lidardir + '05a_lastile_rm_buffer_coarse/'
    else:
        lof = lof_text(lastoolsdir, lidardir + '04_lasclassify/')
        odir = lidardir + '05_lastile_rm_buffer/'

    cmd('%slastile.exe -lof %s -cores %i -remove_buffer -odir %s -olas' % (lastoolsdir, lof, cores, odir))

    if ground_poly != '':
        lof = lof_text(lastoolsdir, lidardir + '04b_lasclassify_fine/')
        odir = lidardir + '05b_lastile_rm_buffer_fine/'

        cmd('%slastile.exe -lof %s -cores %i -remove_buffer -odir %s -olas' % (lastoolsdir, lof, cores, odir))

    logging.info('OK')


    # separate into files for each class type
    logging.info('Separating points by class type on coarse setting...')

    # coarse
    if ground_poly != '':
        lof = lof_text(lastoolsdir, lidardir + '05a_lastile_rm_buffer_coarse/')
        podir = lidardir + '06a_separated_coarse'
    else:
        lof = lof_text(lastoolsdir, lidardir + '05_lastile_rm_buffer/')
        podir = lidardir + '06_separated'

    for class_type in classes:
        odir = podir + '/' + class_type + '/'
        class_code = int(class_type.split('-')[0])
        cmd('%slas2las.exe -lof %s -cores %i -keep_classification %i -odir %s -olas' % (
            lastoolsdir, lof, cores, class_code, odir))

    logging.info('OK')

    if ground_poly == '' and (keep_orig_pts == False):
        ground_results = podir + '/' + '02-Ground' + '/'
        veg_results = podir + '/' + '05-Vegetation' + '/'

    if ground_poly != '':
        logging.info('Separating points by class type on fine setting...')

        # fine
        lof = lof_text(lastoolsdir, lidardir + '05b_lastile_rm_buffer_fine/')

        for class_type in classes:
            odir = lidardir + '06b_separated_fine' + '/' + class_type + '/'
            class_code = int(class_type.split('-')[0])
            cmd('%slas2las.exe -lof %s -cores %i -keep_classification %i -odir %s -olas' % (
                            lastoolsdir, lof, cores, class_code, odir))

        logging.info('OK')

    # clip ground data sets with ground polygon
    if ground_poly != '':
        logging.info('Clipping ground points to inverse ground polygon on coarse setting...')

        # keep points outside ground polygon for coarse setting (-interior flag)
        lof = lof_text(lastoolsdir, lidardir + '06a_separated_coarse' + '/' + '02-Ground' + '/')
        odir = lidardir + '07a_ground_clipped_coarse/'

        cmd('%slasclip.exe -lof %s -cores %i -poly %s -interior -donuts -odir %s -olas' % (
            lastoolsdir, lof, cores, ground_poly, odir))

        logging.info('OK')

        logging.info('Clipping ground points to ground polygon on fine setting...')

        # keep points inside ground polygon for fine setting
        lof = lof_text(lastoolsdir, lidardir + '06b_separated_fine' + '/' + '02-Ground' + '/')
        odir = lidardir + '07b_ground_clipped_fine/'

        cmd('%slasclip.exe -lof %s -cores %i -poly %s -donuts -odir %s -olas' % (
            lastoolsdir, lof, cores, ground_poly, odir))

        logging.info('OK')

    # merge processed ground points with original data set ground points
    if keep_orig_pts:
        logging.info('Merging new and original ground points...')
        if ground_poly != '':
            sources = [lidardir + '07a_ground_clipped_coarse/', lidardir + '07b_ground_clipped_fine/',
                       lidardir + '00_separated' + '/' + '02-Ground' + '/']
        else:
            sources = [lidardir + '06_separated' + '/' + '02-Ground' + '/',
                       lidardir + '00_separated' + '/' + '02-Ground' + '/']
    # just use new points
    elif ground_poly != '':
        logging.info('Merging new ground points...')
        sources = [lidardir + '07a_ground_clipped_coarse/', lidardir + '07b_ground_clipped_fine/']

    if keep_orig_pts or (ground_poly != ''):
        lof = lof_text(lastoolsdir, sources)
        odir = lidardir + '08_ground_merged/'
        ground_results = odir # will be overwritten if rm_duplicates block runs
        cmd('%slastile.exe -lof %s -cores %i -o tile.las -tile_size %i -faf -odir %s -olas' % (
            lastoolsdir, lof, cores, tile_size, odir))

        logging.info('OK')

    # remove duplicate ground points
    if keep_orig_pts:
        logging.info('Removing duplicate ground points...')
        lof = lof_text(lastoolsdir, lidardir + '08_ground_merged/')
        odir = lidardir + '09_ground_rm_duplicates/'
        ground_results = odir

        cmd('%slasduplicate.exe -lof %s -cores %i -lowest_z -odir %s -olas' % (lastoolsdir, lof, cores, odir))

        logging.info('OK')

    # merge new veg points
    if ground_poly != '':
        logging.info('Merging new vegetation points from coarse and fine run...')

        sources = [lidardir + '06a_separated_coarse' + '/' + '05-Vegetation' + '/',
                   lidardir + '06b_separated_fine' + '/' + '05-Vegetation' + '/']
        lof = lof_text(lastoolsdir, sources)
        odir = lidardir + '10_veg_new_merged/'

        cmd('%slastile.exe -lof %s -cores %i -o tile.las -tile_size %i -faf -odir %s -olas' % (
            lastoolsdir, lof, cores, tile_size, odir))

        logging.info('OK')

        # clip new veg points
        # keeping points outside the ground polygon

        logging.info('Clipping new vegetation points...')

        lof = lof_text(lastoolsdir, lidardir + '10_veg_new_merged/')
        odir = lidardir + '11_veg_new_clipped/'

        cmd('%slasclip.exe -lof %s -cores %i -poly %s -interior -donuts -odir %s -olas' % (
            lastoolsdir, lof, cores, ground_poly, odir))

        logging.info('OK')

    # merge with original veg points
    if keep_orig_pts:
        logging.info('Merging new and original vegetation points...')
        if ground_poly != '':
            sources = [lidardir + '11_veg_new_clipped/', lidardir + '00_separated' + '/' + '05-Vegetation' + '/']
        else:
            sources = [lidardir + '06_separated' + '/' + '05-Vegetation' + '/',
                       lidardir + '00_separated' + '/' + '05-Vegetation' + '/']
    elif ground_poly != '':
        logging.info('Retiling new vegetation points...')
        sources = [lidardir + '11_veg_new_clipped/']

    if (keep_orig_pts == True) or (ground_poly != ''):
        lof = lof_text(lastoolsdir, sources)
        odir = lidardir + '12_veg_merged/'
        veg_results = odir # will be overwritten if rm_duplicates block runs

    cmd('%slastile.exe -lof %s -cores %i -o tile.las -tile_size %i -faf -odir %s -olas' % (
        lastoolsdir, lof, cores, tile_size, odir))

    logging.info('OK')

    # remove duplicate veg points
    if keep_orig_pts:
        logging.info('Removing duplicate vegetation points...')

        lof = lof_text(lastoolsdir, lidardir + '12_veg_merged/')
        odir = lidardir + '13_veg_rm_duplicates/'
        veg_results = odir

        cmd('%slasduplicate.exe -lof %s -cores %i -lowest_z -odir %s -olas' % (lastoolsdir, lof, cores, odir))

        logging.info('OK')

    logging.info('Processing finished.')
    logging.info('Outputs in:')
    logging.info('%s\n%s' % (ground_results, veg_results))

    return


def pts(filename, lastoolsdir):
    """returns number of points in las file"""
    # call lasinfo on the file
    cmd('%slasinfo.exe -i %s -otxt -histo number_of_returns 1' % (lastoolsdir, filename))
    # name of txt output file from lasinfo
    txt = filename[:-4] + '.txt'
    f = open(txt, 'r')
    text = f.readlines()
    for line in text:
        if line.endswith('element(s)\n'):
            d = line.split(' ')
            d = d[d.index('for') + 1]
            return int(d)


def r_to_z(r):
    return 0.5 * np.log((1+r)*1.0/(1-r))


def r_confidence_interval(r, n, alpha=0.05):
    """Retrieves the confidence interval at the 1-alpha level for correlation of r with n observations
    when alpha=0.05, it returns the range of possible population correlations at the 95% confidence level
    so if 0 is not within the bounds, then the correlation is statistically significant at the 95% level

    :param r: correlation (float)
    :param n: number of observations (int)
    :param alpha: confidence level (float)
    :return: Confidence interval (low and high) as sequence (list or tuple) of floats.
    """
    if r == 1:
        return 1, 1
    z = r_to_z(r)
    se = 1.0 / np.sqrt(n - 3)
    z_crit = stats.norm.ppf(1 - alpha / 2)  # 2-tailed z critical value

    lo = z - z_crit * se
    hi = z + z_crit * se

    return z_to_r(lo), z_to_r(hi)



def white_noise_confidence_interval(n):
    return -1.0/n - 2.0/np.sqrt(n), -1.0/n + 2.0/np.sqrt(n)


def white_noise_acf_ci(series, maxlags=''):
    """Returns the 95% confidence interval for white noise ACF"""
    n = len(series)
    if maxlags == '':
        maxlags = int(n/2)
    lags = range(maxlags+1)
    lims = [white_noise_confidence_interval(n-k) for k in lags]
    lower_lims, upper_lims = list(zip(*lims))
    return lags, lower_lims, upper_lims


def z_to_r(z):
    return (np.exp(2*z)-1)*1.0/(np.exp(2*z) + 1)