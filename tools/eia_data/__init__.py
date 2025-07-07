"""
EIA (Energy Information Administration) data tools

This module provides tools for accessing energy-related data from the EIA.
"""

from .eia_elec_rates import get_electricity_rates

__all__ = [
    'get_electricity_rates'
]