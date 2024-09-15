# __init__.py

# Standard Library Imports
import logging
import os

# Package-wide Imports
from .strategies import strategies
from .config import ConfigManager
from .data_loader import load_data
from .indicators import calculate_indicators
from .backtest import run_backtest
from .risk_management import RiskManager

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handler (console/file based depending on preference)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('strategizer.log', mode='w')
file_handler.setLevel(logging.INFO)


def configure_risk_management(self, stop_loss_type=None, stop_loss_amt=None, take_profit_prop=None):
    """
    Configure risk management settings.

    :param stop_loss_type: Type of stop-loss to use (e.g., fixed, trailing).
    :param stop_loss_amt: Amount or percentage for stop-loss.
    :param take_profit_prop: Take-profit percentage or amount.
    """
    self.risk_manager.set_parameters(stop_loss_type, stop_loss_amt, take_profit_prop)
    logger.info(f"Risk management updated: Stop Loss Type: {stop_loss_type}, Stop Loss Amt: {stop_loss_amt}, Take Profit Prop: {take_profit_prop}")


def available_strategies(self):
    """
    Return a list of available strategies.

    :return: List of strategy names.
    """
    return list(strategies.keys())


def set_configuration(self, **kwargs):
    """
    Set configuration parameters for the Strategizer instance.

    :param kwargs: Arbitrary configuration options to be set.
    """
    for key, value in kwargs.items():
        if hasattr(self, key):
            setattr(self, key, value)
            logger.info(f"Set configuration {key} to {value}")
        else:
            logger.warning(f"{key} is not a recognized configuration option.")


# Exported functions and classes
__all__ = [
    "Strategizer",
    "strategies",
    "ConfigManager",
    "RiskManager",
    "run_backtest",
    "load_data",
    "calculate_indicators",
]

# Initialize default Strategizer instance for package-level use
strategizer = Strategizer()
