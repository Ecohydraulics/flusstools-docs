""" This module contains the functions called by main.
"""


from config import *


def plot_funs(dc_param_range, dc_fuzzy_funs, dc_disfuzzy_funs):
    """
    Function to plot the membership functions of the parameters and defuzzyfication membership functions into one plot.

    Args:
        dc_param_range (dict): arrays of float values of the six parameters defined into utils.generate_ranges()
        dc_fuzzy_funs (dict): arrays of membership fuzzy functions values of the given ranges of the six parameters
        dc_disfuzzy_funs (dict): arrays of membership defuzzy functions values of the given ranges of the six parameters

    Returns:
        None
    """

    fig, (ax0, ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=6, figsize=(4, 11))

    # plot fuzzy functions of Fine Sediment Share
    ax0.plot(dc_param_range["fs"], dc_fuzzy_funs["fs_c"], 'gray', linewidth=1.5, label='High')
    ax0.plot(dc_param_range["fs"], dc_fuzzy_funs["fs_nc"], 'gray', linestyle="--", linewidth=1.5, label='Low')
    ax0.set_xlabel("FSF [%]")
    ax0.set_ylabel("\u03BC [-]")
    ax0.legend()
    ax0.set_xlim(left=0)
    ax0.set_ylim(bottom=0)
    ax0.legend(loc="lower right")

    # plot fuzzy functions of hydraulic conductivity
    ax1.plot(dc_param_range["kf"], dc_fuzzy_funs["kf_c"], 'gray', linestyle="--", linewidth=1.5, label='Low')
    ax1.plot(dc_param_range["kf"], dc_fuzzy_funs["kf_nc"], 'gray', linewidth=1.5, label='High')
    ax1.set_xlabel("kf [m/s]")
    ax1.set_xscale("log")
    ax1.set_ylabel("\u03BC [-]")
    ax1.legend()
    ax1.set_ylim(bottom=0)
    ax1.legend(loc="lower right")

    # plot fuzzy functions of porosity
    ax2.plot(dc_param_range["po"] / 100, dc_fuzzy_funs["po_c"], 'gray', linestyle="--", linewidth=1.5, label='Low')
    ax2.plot(dc_param_range["po"] / 100, dc_fuzzy_funs["po_nc"], 'gray', linewidth=1.5, label='High')
    ax2.set_xlabel("n [-]")
    ax2.set_ylabel("\u03BC [-]")
    ax2.legend()
    ax2.set_xlim(left=0)
    ax2.set_ylim(bottom=0)
    ax2.legend(loc="lower right")

    # plot fuzzy functions of IDOC
    ax3.plot(dc_param_range["idoc"], dc_fuzzy_funs["idoc_c"], 'gray', linestyle="--", linewidth=1.5, label='Low')
    ax3.plot(dc_param_range["idoc"], dc_fuzzy_funs["idoc_nc"], 'gray', linewidth=1.5, label='High')
    ax3.set_xlabel("IDOC [mg/L]")
    ax3.set_ylabel("\u03BC [-]")
    ax3.legend()
    ax3.set_xlim(left=0)
    ax3.set_ylim(bottom=0)
    ax3.legend(loc="lower right")

    # plot fuzzy functions of Ratio (Huston & Fox)
    ax4.plot(dc_param_range["ratio"], dc_fuzzy_funs["ratio_c"], 'gray', linestyle="--", linewidth=1.5, label='Bridging')
    ax4.plot(dc_param_range["ratio"], dc_fuzzy_funs["ratio_nc"], 'gray', linewidth=1.5, label='USP')
    ax4.set_xlabel("Ratio (Huston & Fox) [-]")
    ax4.set_ylabel("\u03BC [-]")
    ax4.legend()
    ax4.set_xlim(left=0)
    ax4.set_ylim(bottom=0)
    ax4.legend(loc="lower right")

    # plot defuzzification functions of
    ax5.plot(dc_param_range["doc"], dc_disfuzzy_funs["doc_lo"], 'black', linestyle="-.", linewidth=1.5, label='NC-dfz')
    ax5.plot(dc_param_range["doc"], dc_disfuzzy_funs["doc_md"], 'black', linestyle="-", linewidth=1.5, label='MC-dfz')
    ax5.plot(dc_param_range["doc"], dc_disfuzzy_funs["doc_hi"], 'black', linestyle="--", linewidth=1.5, label='SC-dfz')
    ax5.set_xlabel("Degree of Clogging [-]")
    ax5.set_ylabel("\u03BC [-]")
    ax5.legend()
    ax5.set_xlim(left=0, right=1)
    ax5.set_ylim(bottom=0)
    ax5.legend(loc="lower right")

    plt.tight_layout()
    #plt.savefig(fname="output/fuzzy_functions", dpi=300)

    pass


def compute_bcs(dc_limits):
    """
    Function to compute bs and cs constants that define the sigmoid fuzzy membership functions (y = 1 / (1. + exp[- c * (x - b)]))

    Args:
        dc_limits (dict): thresholds of the membership functions defined in config.py
    Returns:
        dc_b (dict): b values of the membership functions
        dc_c (dict): c values of the membership functions
    """
    parameter_order = ["fs_c", "fs_nc",
                       "kf_c", "kf_nc",
                       "po_c", "po_nc",
                       "idoc_c", "idoc_nc",
                       "ratio_c", "ratio_nc",
                       "df_lo", "df_hi"
                       ]
    dc_b = {}
    dc_c = {}
    for fun in parameter_order:
        strings = list(dc_limits.keys())
        substring1 = fun
        substring2 = "{}_mu_{}".format(fun.split("_")[0], fun.split("_")[1])

        list_l = [string for string in strings if substring1 in string]
        list_mul = [string for string in strings if substring2 in string]

        l = [dc_limits[x] for x in list_l]
        mul = [dc_limits[x] for x in list_mul]

        # compute list of bc constants
        c = -(1 / (l[1] - l[0])) * np.log(((1 - mul[1]) / mul[1]) * (mul[0] / (1 - mul[0])))
        b = l[0] + (1 / c) * np.log(1 / mul[0] - 1)

        # append to the list of constantes
        dc_b.update({"{}_b".format(fun): b})
        dc_c.update({"{}_c".format(fun): c})

    # print constants of membership functions
    df_b = pd.DataFrame.from_dict(data=dc_b, orient="index")
    df_c = pd.DataFrame.from_dict(data=dc_c, orient="index")

    #df_b.to_csv("output/functions_constants/df_b.csv")
    #df_c.to_csv("output/functions_constants/df_c.csv")

    return dc_b, dc_c


def compute_fuzzy_functions(dc, dc_b, dc_c):
    """
    Function to compute bs and cs constants that define the sigmoid fuzzy membership functions (y = 1 / (1. + exp[- c * (x - b)]))

    Args:
        dc_limits (dict): thresholds of the membership functions defined in config.py
        dc_b (dict): b values of the membership functions
        dc_c (dict): c values of the membership functions
    Returns:
        (dict): arrays with the membership values of the fuzzy functions
    """
    fs_c = fuzz.sigmf(dc["fs"], dc_b["fs_c_b"], dc_c["fs_c_c"])
    fs_nc = fuzz.sigmf(dc["fs"], dc_b["fs_nc_b"], dc_c["fs_nc_c"])

    kf_c = fuzz.sigmf(dc["kf"], dc_b["kf_c_b"], dc_c["kf_c_c"])
    kf_nc = fuzz.sigmf(dc["kf"], dc_b["kf_nc_b"], dc_c["kf_nc_c"])

    po_c = fuzz.sigmf(dc["po"], dc_b["po_c_b"], dc_c["po_c_c"])
    po_nc = fuzz.sigmf(dc["po"], dc_b["po_nc_b"], dc_c["po_nc_c"])

    idoc_c = fuzz.sigmf(dc["idoc"], dc_b["idoc_c_b"], dc_c["idoc_c_c"])
    idoc_nc = fuzz.sigmf(dc["idoc"], dc_b["idoc_nc_b"], dc_c["idoc_nc_c"])

    ratio_c = fuzz.sigmf(dc["ratio"], dc_b["ratio_c_b"], dc_c["ratio_c_c"])
    ratio_nc = fuzz.sigmf(dc["ratio"], dc_b["ratio_nc_b"], dc_c["ratio_nc_c"])

    return {"fs_c": fs_c, "fs_nc": fs_nc,
            "kf_c": kf_c, "kf_nc": kf_nc,
            "po_c": po_c, "po_nc": po_nc,
            "idoc_c": idoc_c, "idoc_nc": idoc_nc,
            "ratio_c": ratio_c, "ratio_nc": ratio_nc
            }


def generate_ranges():
    """
    Function to define de ranges of the parameters

    Args:
        None
    Returns:
       (dict): array with the ranges of the parameters
    """

    fs = np.arange(0, 26, 0.1)
    kf = np.arange(0, 10 ** -1, 10 ** -4)
    po = np.arange(0, 31, 0.1)
    idoc = np.arange(0, 16, 0.1)
    ratio = np.arange(0, 56, 0.1)
    doc = np.arange(0, 1.1, 0.01)
    return {"fs": fs,
            "kf": kf,
            "po": po,
            "idoc": idoc,
            "ratio": ratio,
            "doc": doc
            }


def compute_desfuzzy_funs(dc_param_range, dc_b, dc_c):
    """
    Function to compute defuzzification membership functions. The functions for high and low degree of clogging are
    Sigmoids and for medium degree of clogging is Gaussian.
    Args:
        dc_param_range: arrays of float values of the six parameters defined into utils.generate_ranges()
    Returns:
       (dict): arrays with the membership values of the defuzzification functions
    """
    doc_lo = fuzz.sigmf(dc_param_range["doc"], dc_b["df_lo_b"], dc_c["df_lo_c"])
    doc_md = fuzz.gaussmf(dc_param_range["doc"], 0.5, 0.083)
    doc_hi = fuzz.sigmf(dc_param_range["doc"], dc_b["df_hi_b"], dc_c["df_hi_c"])
    return {"doc_lo": doc_lo,
            "doc_md": doc_md,
            "doc_hi": doc_hi
            }


def activate_fuzzy_funs(probe, dc_param_range, dc_fuzzy_funs):
    """
     Function to compute the membership values of the fuzzy functions for the parameters of a real sample.
     Args:
         probe (tuple): float values of the parameters of a sample in the following order (F.S, kf, n, IDOC, ratio)
         dc_param_range (dict): arrays of float values of the six parameters defined into utils.generate_ranges()
         dc_fuzzy_funs (dict): arrays with the membership values of the fuzzy functions

     Returns:
        dc_fuzzy_activated (dict): fuzzy membership float values corresponding to the parameter values of the real sample
     """
    parameters = ["fs", "kf", "po", "idoc", "ratio"]

    dc_fuzzy_activated = {}
    for k, par in enumerate(parameters):
        # define what is low or high
        if par == "fs":
            low = "nc"
            high = "c"
        else:
            low = "c"
            high = "nc"

        # Activate membership with values of the probe
        low_level = fuzz.interp_membership(dc_param_range[par],
                                           dc_fuzzy_funs["{}_{}".format(par, low)],
                                           probe[k])
        high_level = fuzz.interp_membership(dc_param_range[par],
                                            dc_fuzzy_funs["{}_{}".format(par, high)],
                                            probe[k])
        dc_fuzzy_activated.update({"{}_{}_low".format(par, low): low_level,
                                   "{}_{}_high".format(par, high): high_level})
    return dc_fuzzy_activated


def plot_aggregation(dc_param_range, dc_mu_desfuzzy, dc_desfuzzy_funs, activation
                     , degree_of_clogging, aggregated, step):
    """
     Function to compute the membership values of the fuzzy functions for the parameters of a real sample.
     Args:
         dc_param_range (dict): arrays of float values of the six parameters defined into utils.generate_ranges()
         dc_mu_desfuzzy (dict): defuzzified membership float values corresponding to the parameter values
          of the real sample
         dc_desfuzzy_funs (dict): arrays with the membership values of the defuzzification functions
         activation (float): degree of clogging that equals to the center of mass of tha sum of the areas under
         the activated defuzzification functions
         degree_of_clogging (float): degree of clogging correct between 0 and 1 in utils.correct_degree_of_clogging()
         aggregated (array): membership float values that define the summed area below the
         activated defuzzification functions.
         step (int): integer that represents the nth sample
     Returns:
        None
     """
    x0 = np.zeros_like(dc_param_range["doc"])

    fig, (ax0, ax1) = plt.subplots(nrows=2, figsize=(5, 5))

    ax0.fill_between(dc_param_range["doc"], x0, dc_mu_desfuzzy["mu_nc"], facecolor='gray', alpha=1)
    ax0.plot(dc_param_range["doc"], dc_desfuzzy_funs["doc_lo"], 'black', linewidth=1.5, linestyle='-.',
             label="NC-dfz")

    ax0.fill_between(dc_param_range["doc"], x0, dc_mu_desfuzzy["mu_mc"], facecolor='gainsboro', alpha=0.7)
    ax0.plot(dc_param_range["doc"], dc_desfuzzy_funs["doc_md"], 'black', linewidth=1.5, linestyle='-', label="MC-dfz")

    ax0.fill_between(dc_param_range["doc"], x0, dc_mu_desfuzzy["mu_sc"], facecolor='black', alpha=0.7)
    ax0.plot(dc_param_range["doc"], dc_desfuzzy_funs["doc_hi"], 'black', linewidth=1.5, linestyle='--', label="SC-dfz")
    ax0.set_xlabel("Degree of Clogging [-]")
    ax0.set_ylabel("\u03BC [-]")
    ax0.set_xlim(left=0, right=1)
    ax0.set_ylim(bottom=0)
    ax0.legend(loc="lower right")

    # fill aggregated functions
    ax1.plot(dc_param_range["doc"], dc_desfuzzy_funs["doc_lo"], 'black', linewidth=1.5, linestyle='-.',
             label="NC-dfz")
    ax1.plot(dc_param_range["doc"], dc_desfuzzy_funs["doc_md"], 'black', linewidth=1.5, linestyle='-', label="MC-dfz")
    ax1.plot(dc_param_range["doc"], dc_desfuzzy_funs["doc_hi"], 'black', linewidth=1.5, linestyle='--', label="SC-dfz")
    ax1.fill_between(dc_param_range["doc"], x0, aggregated, facecolor='gray', alpha=0.8)
    ax1.plot([degree_of_clogging, degree_of_clogging], [0, 0.7 * activation], 'k', linewidth=1.5, alpha=0.9)
    ax1.set_xlabel("Aggregated membership and result (line)")
    ax1.set_ylabel("\u03BC [-]")
    ax1.set_xlim(left=0, right=1)
    ax1.set_ylim(bottom=0)
    ax1.legend(loc="lower right")

    # Turn off top/right axes
    for ax in (ax0, ax1):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()
    #plt.savefig(fname="output/aggregation/sample_{}".format(step + 1), dpi=300)
    pass


def apply_fuzzy_rules(dc_af=None, dc_desfuzzy_funs=None, centroid=False, mu_list=None):
    """
     Function to choose membership value of defuzzification functions based on the fuzzy rules.

     Args:
         dc_af (dict): membership values of fuzzy functions of a sample
         dc_desfuzzy_funs (dict): arrays with the membership values of the defuzzification functions
         centroid (boolean): True to correct the limits of degree of clogging to [0,1]
         mu_list (list): corrected membership function values of the activated defuzzification functions

     Returns:
        dc_mu_defuzzy (dict): array of membership values that define area under the curve of the defuzzification
        functions
        dc_mu_defuzzy_values (dict): three float values of the sample-activated defuzzification functions
     """
    if centroid:
        mu_sc_value = mu_list[2]
        mu_mc_value = mu_list[1]
        mu_nc_value = mu_list[0]
    else:

        mu_sc_value = max([np.fmin(dc_af["kf_c_low"], dc_af["fs_c_high"]),
                           np.fmin(dc_af["po_c_low"], dc_af["fs_c_high"]),
                           np.fmin(dc_af["kf_c_low"], dc_af["ratio_c_low"])]
                          )

        mu_mc_value = max([np.fmin(dc_af["kf_c_low"], dc_af["idoc_nc_high"]),
                           np.fmin(dc_af["fs_c_high"], (1 - dc_af["kf_c_low"]))]
                          )

        mu_nc_value = max([np.fmin(dc_af["idoc_nc_high"], dc_af["kf_nc_high"]),
                           np.fmin(dc_af["kf_nc_high"], dc_af["fs_nc_low"]),
                           np.fmin(dc_af["ratio_nc_high"], dc_af["kf_nc_high"])]
                          )
    # class moderate clogging
    mu_mc = np.fmin(mu_mc_value,
                    dc_desfuzzy_funs["doc_md"]
                    )
    # class strong clogging
    mu_sc = np.fmin(mu_sc_value,
                    dc_desfuzzy_funs["doc_hi"]
                    )
    # class no clogging
    mu_nc = np.fmin(mu_nc_value,
                    dc_desfuzzy_funs["doc_lo"]
                    )
    # dict with memberships of defuzzified functions
    dc_mu_defuzzy = {"mu_sc": mu_sc,
                      "mu_mc": mu_mc,
                      "mu_nc": mu_nc,
                     }
    dc_mu_defuzzy_values = {"mu_sc": mu_sc_value,
                             "mu_mc": mu_mc_value,
                             "mu_nc": mu_nc_value, }

    return dc_mu_defuzzy, dc_mu_defuzzy_values


def find_centroids(dc_desfuzzy_funs, dc_param_range):
    """
     Function to find centroids of the non clogging and strong clogging defuzzification functions

     Args:
         dc_param_range (dict): arrays of float values of the six parameters defined into utils.generate_ranges()
         dc_desfuzzy_funs (dict): arrays with the membership values of the defuzzification functions
     Returns:
         dc_defuzzy_centroids (dict): two float values that represent the centroids of sc and nc defuzzi-functions
     """
    mu_list_nc = [0.99, 0.01, 0.01]
    mu_list_sc = [0.01, 0.01, 0.99]
    mu_lists = [mu_list_nc, mu_list_sc]
    dic_defuzzy_centroids = {}
    for k, mu_list in enumerate(mu_lists):
        dc_mu_desfuzzy, _ = apply_fuzzy_rules(None, dc_desfuzzy_funs,
                                              True, mu_list)
        aggregated = np.fmax(dc_mu_desfuzzy["mu_sc"],
                             np.fmax(dc_mu_desfuzzy["mu_mc"], dc_mu_desfuzzy["mu_nc"]))
        centroid = fuzz.defuzz(dc_param_range["doc"], aggregated, 'centroid')
        if k == 0:
            name = "nc"
        else:
            name = "sc"
        dic_defuzzy_centroids.update({"{}_centroid".format(name): centroid})

    return dic_defuzzy_centroids


def correct_degree_of_clogging(dc_defuzzy_centroids, degree_of_clogging):
    """
     Function to correct degree of clogging from the interval [centroid_of_no_clogging, centroid_of_strong_clogging]
     to [0, 1]

     Args:
         degree_of_clogging (float): original degree of clogging
         dc_defuzzy_centroids (dict): two float values that represent the centroids of sc and nc defuzzi-functions
     Returns:
         degree_of_clogging_corrected (float): degree of clogging in the interval [0, 1]
     """
    # define limits of old and new scale
    old_scale_low_limit = dc_defuzzy_centroids["nc_centroid"]
    old_scale_high_limit = dc_defuzzy_centroids["sc_centroid"]

    # transform de scale linearly to [0,1] scale and compute corrected degree of clogging

    degree_of_clogging_corrected = (degree_of_clogging - old_scale_low_limit) \
                                   / (old_scale_high_limit - old_scale_low_limit)

    return degree_of_clogging_corrected


def add_columns(df_samples):
    """
     Function to add columns of csv output

     Args:
         df_samples (Dataframe): dataframe with the parameters of the samples
     Returns:
         df_samples (Dataframe): same input Dataframe but with new columns
     """
    columns = ["dc_c", "dc",  # degree of clogging corrected and initial
               "mu_nc", "mu_mc", "mu_sc",  # membership of defuzzified functions
               "mu_fsf_low", "mu_fsf_high",  # membership of fuzzy functions
               "mu_kf_low", "mu_kf_high",
               "mu_n_low", "mu_n_high",
               "mu_idoc_low", "mu_idoc_high",
               "mu_ratio_low", "mu_ratio_high"
               ]
    df_samples[columns] = np.nan

    return df_samples


def add_results(df, step, degree_of_clogging_corrected, degree_of_clogging, dc_mu_desfuzzy_values, dc_af):
    """
     Function to add computed result to output-Dataframe

     Args:
         df (Dataframe): input Dataframe
         step (int): nth sample
         degree_of_clogging_corrected (float): dregree of clogging corrected to interval [0, 1]
         degree_of_clogging (float): degree of clogging in the
         interval [centroid_of_no_clogging, centroid_of_strong_clogging]
         dc_mu_desfuzzy_values (dict): three float values of the sample-activated defuzzification functions
         dc_af (dict): membership float values of the activated fuzzy functions
         step (int): nth sample
     Returns:
         df (Dataframe): output Dataframe
     """
    # add degree of clogging
    df.loc[step, ["dc_c", "dc"]] = [degree_of_clogging_corrected, degree_of_clogging]

    # add membership functions of defuzzification functions
    df.loc[step, ["mu_nc", "mu_mc", "mu_sc"]] = [dc_mu_desfuzzy_values["mu_nc"],
                                                 dc_mu_desfuzzy_values["mu_mc"],
                                                 dc_mu_desfuzzy_values["mu_sc"]
                                                 ]
    for i, mu in enumerate(dc_af.values()):
        df.iloc[step, (i + 12)] = mu
    return df
