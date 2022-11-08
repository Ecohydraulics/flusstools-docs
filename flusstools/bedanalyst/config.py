""" This module contains all the imported packages (dependencies) and
user inputs for running the main script.

The first input is the dictionary containing two points for the fuzzy and defuzzification functions.
Two points define a function and the have the following format:

(parameter_values, corresponding_membership_values)

For example, for the parameter fine sediment share, the point with the lowest value in the y-axis
is written as follows:

(fs_c_llow, fs_mu_c_llow)

where fs stands for fine sediment share, c indicates the membership function associated to clogging,
mu indicates the membership value, and llow indicates the relative position of the point in the curve.

The second input is the local address of the csv file containing the parameters of the samples.

The third input is composed by two booleans that indicates the algorithm to print the fuzzy functions
and the aggregation functions inside the folder output.
"""


# Define the limits of the parameters and membership functions
dc_limits = {  # fine sediment
                "fs_c_llow ": 8, "fs_c_lhigh": 20, "fs_nc_llow": 1, "fs_nc_lhigh": 11.3,
                "fs_mu_c_llow ": 0.1, "fs_mu_c_lhigh": 0.9, "fs_mu_nc_llow": 0.99, "fs_mu_nc_lhigh": 0.1,
                # hydraulic conductivity
                "kf_c_llow ": 2 * 10 ** -5, "kf_c_lhigh": 5.56 * 10 ** -3, "kf_nc_llow": 10 ** -4, "kf_nc_lhigh": 2.78 * 10 ** -3,
                "kf_mu_c_llow ": 0.99, "kf_mu_c_lhigh": 0.1, "kf_mu_nc_llow": 0.1, "kf_mu_nc_lhigh": 0.99,
                # porosity
                "po_c_llow ": 6, "po_c_lhigh": 15, "po_nc_llow": 15, "po_nc_lhigh": 26.2,
                "po_mu_c_llow ": 0.9, "po_mu_c_lhigh": 0.1, "po_mu_nc_llow": 0.1, "po_mu_nc_lhigh": 0.9,
                # IDOC
                "idoc_c_llow ": 6, "idoc_c_lhigh": 1, "idoc_nc_llow": 3, "idoc_nc_lhigh": 10,
                "idoc_mu_c_llow ": 0.1, "idoc_mu_c_lhigh": 0.9, "idoc_mu_nc_llow": 0.1, "idoc_mu_nc_lhigh": 0.9,
                # Ratio dss/(dfs*omega_ss)
                "ratio_c_llow ": 10, "ratio_c_lhigh": 27, "ratio_nc_llow": 27, "ratio_nc_lhigh": 44.8,
                "ratio_mu_c_llow ": 0.99, "ratio_mu_c_lhigh": 0.1, "ratio_mu_nc_llow": 0.1, "ratio_mu_nc_lhigh": 0.9,
                # low/high defuzzification
                "df_lo_llow ": 0, "df_lo_lhigh": 0.5, "df_hi_llow": 0.5, "df_hi_lhigh": 1,
                "df_mu_lo_llow ": 0.99, "df_mu_lo_lhigh": 0.1, "df_mu_hi_llow": 0.1, "df_mu_hi_lhigh": 0.99,
}

