from enum import Enum, auto
from typing import Sequence

import numpy as np
from numpy.lib.nanfunctions import nanmean

class ScoreMode(Enum):
    """The method by which to calculate a score from multiple possible scores.
    Used when calculating an overall docking score from multiple conformations,
    multiple repeated runs, or docking against an ensemble of receptors."""
    AVG = auto()
    BEST = auto()
    BOLTZMANN = auto()
    TOP_K_AVG = auto()

def calc_score(
    scores: Sequence[float],
    score_mode: ScoreMode = ScoreMode.BEST, k: int = 1
) -> float:
    """Calculate an overall score from a sequence of scores

    Parameters
    ----------
    scores : Sequence[float]
    score_mode : ScoreMode, default=ScoreMode.BEST
        the method used to calculate the overall score. See ScoreMode for
        choices
    k : int, default=1
        the number of top scores to average, if using ScoreMode.TOP_K_AVG

    Returns
    -------
    float
    """
    Y = np.array(scores)

    if score_mode == ScoreMode.BEST:
        return Y.min()
    elif score_mode == ScoreMode.AVG:
        return np.nanmean(Y)
    elif score_mode == ScoreMode.BOLTZMANN:
        Y_e = np.exp(-Y)
        Z = Y_e / np.nansum(Y_e)
        return np.nansum(Y * Z)
    elif score_mode == ScoreMode.TOP_K_AVG:
        return np.nanmean(Y.sort()[:k])
        
    return Y.min()