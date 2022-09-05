import os
import math
import numpy as np
import flopy.modflow as fpm
import pandas as pd
import flopy.utils.binaryfile as bf
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter


df_input = pd.read_excel('dc-only-logs.xlsx',
                         usecols=['depth', 'dc_c', 'id'])

# Create array for subsequent loop
meas_array = df_input['id'].unique().tolist()

nested_colors = {'us': 'grey', 'ds': 'black', None: 'black'}

nested_markers = {'before': 'd', 'after': 's'}

df_input[['location', 'campaign']] = df_input['id'].str.split(' ', expand=True)
df_input[['site', 'up or downstream']] = df_input['location'].str.split('-', expand=True)

# Loop through measurement location
for site in df_input['site'].unique().tolist():
    fig, ax = plt.subplots(figsize=(3.5, 5.25))
    meas_array_site = df_input[df_input['site'] == site]
    meas_array_site_list = meas_array_site['id'].unique().tolist()
    # for each measurement location loop through kf values computed with different qapproaches
    for meas in meas_array_site_list:
        df_toplot = df_input[df_input['id'] == meas]
        campaign, up_or_down = df_toplot['campaign'].iloc[0], df_toplot['up or downstream'].iloc[0]
        df_toplot.plot(x='dc_c',
                       y='depth',
                       color=nested_colors[up_or_down],
                       ax=ax,
                       label=meas,
                       grid=True,
                       marker=nested_markers[campaign])
    ax.set_xlabel('Degree of Clogging [-]')
    ax.set_ylabel('Riverbed depth [m]')
    ax.xaxis.set_label_position('top')  # axis label is located on the top, instead of on the bottom as usual
    ax.xaxis.tick_top()
    ax.set_ylim(bottom=0.6, top=0)
    # ax.xaxis.set_major_formatter(FormatStrFormatter('%1.0e'))
    ax.set_xlim(0, 1)
    ax.legend(loc='center left', bbox_to_anchor=(0, 0.1))
    plt.tight_layout()
    fig.savefig('output/' + site + '_dc.png', dpi=300)
