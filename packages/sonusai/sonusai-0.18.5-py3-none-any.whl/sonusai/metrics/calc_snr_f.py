import numpy as np

from sonusai.mixture.datatypes import Segsnr
from sonusai.mixture.datatypes import SnrFMetrics


def calc_snr_f(segsnr_f: Segsnr) -> SnrFMetrics:
    """Calculate metrics of snr_f truth data.

    For now, includes mean and variance of the raw values (usually energy)
    and mean and standard deviation of the dB values (10 * log10).
    """
    if np.count_nonzero(segsnr_f) == 0:
        # If all entries are zeros
        return SnrFMetrics(0, 0, -np.inf, 0)

    tmp = np.ma.array(segsnr_f, mask=np.logical_not(np.isfinite(segsnr_f)), dtype=np.float32)
    if np.ma.count_masked(tmp) == np.ma.size(tmp, axis=0):
        # If all entries are infinite
        return SnrFMetrics(np.inf, 0, np.inf, 0)

    snr_mean = np.mean(tmp, axis=0)
    snr_var = np.var(tmp, axis=0)

    tmp = 10 * np.ma.log10(tmp)
    if np.ma.count_masked(tmp) == np.ma.size(tmp, axis=0):
        # If all entries are masked, special case where all inputs are either 0 or infinite
        snr_db_mean = -np.inf
        snr_db_std = np.inf
    else:
        snr_db_mean = np.mean(tmp, axis=0)
        snr_db_std = np.std(tmp, axis=0)

    return SnrFMetrics(snr_mean, snr_var, snr_db_mean, snr_db_std)
