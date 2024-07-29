"""An example application for calculating the degree of clogging based on the parameters:
- Fine sediment share ('FSS') < 1mm [%] of riverbed samples
- Porosity of the riverbed samples ('n') [-]
- Hydraulic conductivity ('kf') [m/s]
- Interstitial dissolved oxygen concentration ('IDOC') [mg/L]
- Adjusted bridging criterion according to Huston & Fox (2015) ('ratio') [-], doi: 10.1061/(ASCE)HY.1943-7900.0001015,
calculated as d_ss/(d_fs*sigma_ss), where d_ss and d_fs is the geometric mean grain size of substrate sediments and fine
sediments, respectively, and sigma_ss is the geometric standard deviation of grain sizes of substrate sediments.
which should be entered as columns with the column names as described in the file inputs-realdata.csv. The output
fuzzy degrees of clogging are saved as csv.

"""

import flusstools.bed_analyst as bea


# read a cvs file into a dataframe (global variable)
df_samples = pd.read_csv("inputs-realdata.csv")
df_samples = df_samples.iloc[:, 0:7]

bea.degree_clogging.degree_clogging(df_samples, "output/output.csv")
