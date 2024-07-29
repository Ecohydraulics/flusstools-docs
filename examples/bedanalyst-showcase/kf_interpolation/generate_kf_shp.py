from flusstools import bed_analyst

columns = ['kf_10cm_corr',
               'kf_15cm_corr',
               'kf_20cm_corr',
               'kf_25cm_corr',
               'kf_30cm_corr',
               'kf_40cm_corr',
               'kf_50cm_corr',
               'kf_60cm_corr']

new_depths = np.array([0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6])
meas_at_cols = ('depth_correc [m]', 'kf (Wooster et al. (2008)) [m/s]')
lonlat = ('lon', 'lat')

# read excel as df
df = pd.read_excel('slurp-data.xlsx', engine='openpyxl', skiprows=[1])

bed_analyst.interp_z2shp(df,
             lonlat=lonlat,
             crs='epsg:3857',
             sample_column='sample',
             interp_at_z_stamps=new_depths,
             new_attr_names=columns,
             meas_at_cols=meas_at_cols,
             path_shp='trial.shp')