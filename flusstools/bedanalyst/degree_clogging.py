""" This module calls the necessary functions to perform the computation
of degree of clogging.
"""

from config import *
from utils import *


def degree_clogging(df_samples, output_csv_path, plot=[False, False]):
    """
    Function for computing degree of clogging using the input riverbed parameter along the riverbed depth:
        + Fine Sediment Saare/Fraction (fsf/fss): [%]
        + Hydraulic Conductivity (kf): [m/s]
        + Porosity (n): [-]
        + Interstitial Dissolved Oxygen Content (IDOC): [mg/L]
        + Bridging criterion according to Huston & Fox (2015; referred as 'ratio' here): [-]

    Args:
        df_samples (pandas.DataFrame): df containing the columns 'id' (sample id), 'fss', 'kf', 'n', 'idoc' and 'ratio'
        output_csv_path (str): path to output csv containing the results of the fuzzy inference and final computed degree
            of clogging
        plot (list): List of two boolean objects indicating if the plots for the aggregation function and the fuzzy
        membership functions of the above mentione dparameters is required. Should be True if required, respectively.

    Returns:
        None
    """
    # Take list of probes as tuples
    df_par = df_samples.drop(["id"], axis=1)
    probes = df_par.to_records(index=False)

    # Add columns for membership values and dregree of cloggging
    df_samples = add_columns(df_samples)

    # Compute b and c constants to define membership functions
    dc_b, dc_c = compute_bcs(dc_limits=dc_limits)

    # Generate universe variables
    dc_param_range = generate_ranges()

    # Generate fuzzy membership functions
    dc_fuzzy_funs = compute_fuzzy_functions(dc_param_range, dc_b, dc_c)

    # Generate low and high defuzzification functions
    dc_desfuzzy_funs = compute_desfuzzy_funs(dc_param_range, dc_b, dc_c)

    for step, probe in enumerate(probes):
        # Activate fuzzy functions
        dc_af = activate_fuzzy_funs(probe, dc_param_range, dc_fuzzy_funs)

        # Create fuzzy rules
        dc_mu_desfuzzy, dc_mu_desfuzzy_values = apply_fuzzy_rules(dc_af, dc_desfuzzy_funs)

        # Defuzzification
        aggregated = np.fmax(dc_mu_desfuzzy["mu_sc"],
                             np.fmax(dc_mu_desfuzzy["mu_mc"], dc_mu_desfuzzy["mu_nc"]))

        # Calculate defuzzified result
        degree_of_clogging = fuzz.defuzz(dc_param_range["doc"], aggregated, 'centroid')
        activation = fuzz.interp_membership(dc_param_range["doc"], aggregated, degree_of_clogging)  # for plot

        # Compute sigmoid centroids to new scale of desfuzzy functions
        dic_desfuzzy_centroids = find_centroids(dc_desfuzzy_funs, dc_param_range)

        # Correct degree of clogging into new scale
        degree_of_clogging_corrected = correct_degree_of_clogging(dic_desfuzzy_centroids, degree_of_clogging)

        # save computed values into a dataframe
        df_samples = add_results(df_samples,
                                 step,
                                 degree_of_clogging_corrected,
                                 degree_of_clogging,
                                 dc_mu_desfuzzy_values,
                                 dc_af
                                 )

        # Plot aggregation of areas and crisp values (degree of clogging)
        plot_aggregation(dc_param_range, dc_mu_desfuzzy,
                         dc_desfuzzy_funs, activation,
                         degree_of_clogging, aggregated, step) if plot[0] else None

    # Plot membership functions
    plot_funs(dc_param_range, dc_fuzzy_funs, dc_desfuzzy_funs) if plot[1] else None

    # save the computed values into a csv
    df_samples.to_csv(output_csv_path)

