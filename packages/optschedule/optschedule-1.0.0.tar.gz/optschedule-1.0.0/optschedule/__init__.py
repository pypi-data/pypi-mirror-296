"""
OptSchedule

Flexible parameter scheduler that can be implemented with proprietary and open source optimizers and algorithms.
"""

from optschedule.schedule import *
from optschedule.oop_schedule import Schedule

__all__ = [s for s in dir() if not s.startswith("_")]

__version__ = "1.0.0"
__author__ = "draktr"
