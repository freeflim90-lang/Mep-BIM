import numpy as np
import pandas as pd


def generate_virtual_energy_data(
    start_date: str = "2024-01-01",
    periods: int = 24 * 365 * 2,
    freq: str = "h",
    seed: int = 42,
) -> pd.DataFrame:
    """
    Create a realistic virtual hourly energy dataset.

    The simulation includes:
    - Daily usage behavior (morning/evening peaks)
    - Weekly pattern (weekend drop)
    - Yearly seasonality
    - Weather-driven HVAC load
    - Mild growth trend and random noise
    """
    rng = np.random.default_rng(seed)
    index = pd.date_range(start=start_date, periods=periods, freq=freq)

    hour = index.hour.to_numpy()
    day_of_week = index.dayofweek.to_numpy()
    day_of_year = index.dayofyear.to_numpy()

    morning_peak = 22 * np.exp(-0.5 * ((hour - 8) / 2.3) ** 2)
    evening_peak = 34 * np.exp(-0.5 * ((hour - 19) / 3.0) ** 2)
    night_drop = -10 * np.exp(-0.5 * ((hour - 3) / 1.9) ** 2)

    annual_pattern = 12 * np.sin(2 * np.pi * day_of_year / 365)
    weekend_effect = np.where(day_of_week >= 5, -9, 0)
    long_term_trend = np.linspace(0, 4, periods)

    temperature = (
        23
        + 9.5 * np.sin(2 * np.pi * (day_of_year - 28) / 365)
        + 4.0 * np.sin(2 * np.pi * (hour - 14) / 24)
        + rng.normal(0, 1.3, periods)
    )
    cooling_load = np.maximum(temperature - 24, 0) * 2.8
    heating_load = np.maximum(15 - temperature, 0) * 1.7

    noise = rng.normal(0, 4.8, periods)

    energy = (
        112
        + morning_peak
        + evening_peak
        + night_drop
        + annual_pattern
        + weekend_effect
        + long_term_trend
        + cooling_load
        + heating_load
        + noise
    )
    energy = np.clip(energy, 25, None)

    return pd.DataFrame(
        {
            "Datetime": index,
            "Energy": np.round(energy, 2),
            "Temperature": np.round(temperature, 2),
        }
    )

