"""
eefunction.property
~~~~~~~~~~~~~

This module contains the function to get fluid properties.
"""

# from typing import Dict, Optional, Union
import math
from CoolProp.CoolProp import PropsSI


if __name__ == '__main__':
    print(PropsSI('T', 'T', 273.15 + 25 , 'P', 100e5, 'CO2'))
