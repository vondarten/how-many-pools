import scipy.stats as st
import math

def cochran_sample_size(confidence_level, margin_of_error, estimated_proportion=0.5, population_size=None):
    """
    Calculates the sample size using Cochran's formula.

    Args:
        confidence_level (float): The desired confidence level (e.g., 0.95, 0.99).
        margin_of_error (float): The desired margin of error (e.g., 0.05).
        estimated_proportion (float, optional): The estimated proportion of the
                                                population. Defaults to 0.5.
        population_size (int, optional): The total population size. If provided,
                                        the formula will be adjusted for a finite
                                        population. Defaults to None.

    Returns:
        int: The calculated sample size.
    """

    # Calculate the Z-score from the confidence level
    z_score = st.norm.ppf(1 - (1 - confidence_level) / 2)

    # Calculate the initial sample size for an infinite population
    sample_size_infinite = (z_score**2 * estimated_proportion * (1 - estimated_proportion)) / margin_of_error**2

    # Adjust for a finite population if population_size is provided
    if population_size:
        sample_size_finite = sample_size_infinite / (1 + (sample_size_infinite - 1) / population_size)
        return math.ceil(sample_size_finite)
    else:
        return math.ceil(sample_size_infinite)
