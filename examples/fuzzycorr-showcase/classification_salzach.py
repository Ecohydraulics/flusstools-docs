try:
    import matplotlib.pyplot as plt
    import fuzzycorr.prepro as pp
    from pathlib import Path
    import numpy as np
    import gdal
except:
    print('ModuleNotFoundError: Missing fundamental packages (required: pathlib, numpy, gdal).')


cur_dir = Path.cwd()

Path(cur_dir / "rasters").mkdir(exist_ok=True)

raster_meas = pp.PreProCategorization(str(cur_dir / 'rasters') + '/' + 'vali_meas_2013_res5_clipped.tif')
raster_sim = pp.PreProCategorization(str(cur_dir / 'rasters') + '/' + 'vali_hydro_FT_manual_2013_res5_clipped.tif')

n_classes = 12

nb_classes = np.insert(raster_meas.nb_classes(n_classes), 0, -np.inf, axis=0)
nb_classes[-1] = np.inf

raster_meas.categorize_raster(nb_classes, map_out=str(cur_dir / 'rasters') + '/' + 'vali_meas_class_nbreaks.tif', save_ascii=False)
raster_sim.categorize_raster(nb_classes, map_out=str(cur_dir / 'rasters') + '/' + 'vali_hydro_FT_manual_class_nbreaks.tif', save_ascii=False)
