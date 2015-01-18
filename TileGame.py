#!/usr/bin/env python
# coding=utf-8
""" Module /TileGame.py
    TileGame for Python 3
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame

    Launches the game. For more information, check the file /src/main.py
"""

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "src"))
from src import main

main.main()