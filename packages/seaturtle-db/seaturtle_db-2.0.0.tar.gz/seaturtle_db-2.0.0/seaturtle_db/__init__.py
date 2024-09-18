#                                  .                            .   oooo                              .o8   .o8
#                                .o8                          .o8   `888                             "888  "888
#  .oooo.o  .ooooo.   .oooo.   .o888oo oooo  oooo  oooo d8b .o888oo  888   .ooooo.               .oooo888   888oooo.
# d88(  "8 d88' `88b `P  )88b    888   `888  `888  `888""8P   888    888  d88' `88b             d88' `888   d88' `88b
# `"Y88b.  888ooo888  .oP"888    888    888   888   888       888    888  888ooo888             888   888   888   888
# o.  )88b 888    .o d8(  888    888 .  888   888   888       888 .  888  888    .o             888   888   888   888
# 8""888P' `Y8bod8P' `Y888""8o   "888"  `V88V"V8P' d888b      "888" o888o `Y8bod8P' ooooooooooo `Y8bod88P"  `Y8bod8P'
"""
Python Database Library
-----------------------

seaturtle_db is a library which lets you use python files as databases

:copyright: (c) 2024 by Tathya Garg
:license: MIT, see LICENSE for more details.
"""

from . import database, exceptions

from .database import Database
from .exceptions import *

from .__version__ import (
    __author__,
    __author_email__,
    __copyright__,
    __description__,
    __license__,
    __love__,
    __title__,
    __version__
)
