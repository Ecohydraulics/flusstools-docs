import pandas as pd
from scipy import integrate, interpolate
import numpy as np
import matplotlib.pyplot as plt

# Read as df
df_input = pd.read_excel('dc-for-manuscript.xlsx',
                         usecols=['measurement point', 'Riverbed depth [m]', 'Degree of Clogging [-]'],
                         )

df_input[['location', 'campaign']] = df_input['measurement point'].str.split(' ', expand=True)
df_input[['site', 'up or downstream']] = df_input['location'].str.split('-', expand=True)


for location in ['A-us', 'A-ds', 'B-us', 'B-ds']:

    # filter by site, like A-1, A-2 etc
    meas_array_site = df_input[df_input['location'] == location]

    # filter the sample before the flushing and creates a function as a piecewise linear interp.
    line_1 = meas_array_site[meas_array_site['campaign'] == 'before']
    min_1, max_1 = line_1['Riverbed depth [m]'].min(), line_1['Riverbed depth [m]'].max()
    line_2 = meas_array_site[meas_array_site['campaign'] == 'after']
    min_2, max_2 = line_2['Riverbed depth [m]'].min(), line_2['Riverbed depth [m]'].max()
    min, max = np.max([min_1, min_2]), np.min([max_1, max_2])

    sample_array_1 = line_1['Degree of Clogging [-]'].to_numpy()
    sample_array_depth_1 = line_1['Riverbed depth [m]'].to_numpy()
    f_1 = interpolate.interp1d(sample_array_depth_1,
                               sample_array_1,
                               bounds_error=False,
                               fill_value='extrapolate',
                               assume_sorted=False)
    f_1func = lambda x: f_1(x)
    f_1area = integrate.quad(f_1func, min, max)[0]

    sample_array_2 = line_2['Degree of Clogging [-]'].to_numpy()
    sample_array_depth_2 = line_2['Riverbed depth [m]'].to_numpy()
    f_2 = interpolate.interp1d(sample_array_depth_2,
                               sample_array_2,
                               bounds_error=False,
                               fill_value='extrapolate',
                               assume_sorted=False)
    f_2func = lambda x: f_2(x)
    f_2area = integrate.quad(f_2func, min, max)[0]
    x = np.linspace(min, max, 500)
    fig, ax = plt.subplots()
    plt.plot(x, f_1func(x), x, f_2func(x))
    # plt.fill_between(x, f_1func(x), f_2func(x))
    plt.show()
    area_diff = (f_1area - f_2area)/(max-min)
    print('The normalized area between before- after for {} is {} [-]'.format(location, area_diff))


