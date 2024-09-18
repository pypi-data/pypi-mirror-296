import numpy as np
from bootstrapping_tools import generate_latex_interval_string
from eradication_data_requirements import fit_ramsey_plot


def get_population_status_dict(raw_data, bootstrap_number, seed):
    intercepts_distribution = get_intercepts_distribution(raw_data, bootstrap_number, seed)
    interval = get_confidence_interval(intercepts_distribution)
    n0_interval = generate_latex_interval_string(interval, deltas=False, decimals=0)

    captures = raw_data.Capturas.sum()
    remanentes = remaining_interval(interval, captures)
    remanentes_interval = generate_latex_interval_string(remanentes, deltas=False, decimals=0)
    json_content = {"n0": n0_interval, "remanentes": remanentes_interval, "capturas": int(captures)}
    return json_content


def remaining_interval(n0_interval, captures):
    remanentes = n0_interval - captures
    return [x if x > 0 else 0 for x in remanentes]


def get_confidence_interval(distribution):
    interval = np.percentile(distribution, [2.5, 50, 97.5]).astype(int)
    return interval


def get_intercepts_distribution(raw_data, bootstrap_number, seed=None):
    rng = np.random.default_rng(seed)
    raw_distribution = []
    distribution_size = 0
    captures = raw_data.Capturas.sum()
    while distribution_size < bootstrap_number:
        intercept = calculate_x_intercept(resample_eradication_data(raw_data, rng))
        if intercept > captures:
            raw_distribution.append(intercept)
        distribution_size = len(raw_distribution)
    return raw_distribution


def resample_eradication_data(data, rng):
    resampled_data = data.sample(replace=True, frac=1, random_state=rng)
    sorted_data = resampled_data.sort_index()
    sorted_data["Cumulative_captures"] = sorted_data.Capturas.cumsum()
    return sorted_data[["CPUE", "Cumulative_captures"]]


def calculate_x_intercept(data):
    parameters = fit_ramsey_plot(data)
    return -parameters[1] / parameters[0]
