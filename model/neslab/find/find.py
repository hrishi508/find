import math
import numpy as np
import pandas as pd

def process_csv(path: str):
    """Read the csv and return the optimized scales as an array

    Args:
        path (str): absolute path to the optimized scales csv file

    Returns:
        np.ndarray: optimized scales of geometric distro
    """
    df = pd.read_csv(path, index_col="t_chr")
    df.sort_index(inplace=True)
    df = df.reindex(np.arange(10, df.index[-1] - 30, 10))
    df.interpolate(inplace=True)

    table = df["x_opt"].values.astype(np.float32)

    return table

def lookup_scale(t_chr: int, table: np.ndarray):
    """Returns the optimized scale for the given charging time

    Args:
        t_chr (int): Latest charging time (in slots)
        table (np.ndarray): Table with optimized scale of geometric distro

    Returns:
        float: optimized scale
    """
    if t_chr < 10: return table[0]
    elif t_chr > 2560: return table[255]

    idx_low = int(t_chr/10 - 1)
    val_low = table[idx_low]
    val_high = table[int(t_chr/10)]
    frac = (t_chr % 10)/10

    return val_low + frac * (val_high - val_low)

def geometric_itf_sample(p: float):
    """Return the delay value sampled from geometric distro

    Args:
        p (float): optimized scale for geometric distro

    Returns:
        int: randomly sampled delay
    """
    y = np.random.uniform()
    res = int(math.log(1 - y)/math.log(1 - p) - 1)

    return res

def Find(path: str, t_chr: int):
    """Calculate the random waiting time given the latest current charging time

    Args:
        path (str): absolute path to the optimized scales csv file
        t_chr (int): Latest charging time (in slots)

    Returns:
        int: waiting time (in slots)
    """
    table = process_csv(path)
    wait_time = geometric_itf_sample(lookup_scale(t_chr, table))

    return wait_time
