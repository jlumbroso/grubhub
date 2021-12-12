"""
A quick wrapper around GrubHub's API, to fetch account and order information.
"""

from grubhub.client import GrubHubClient

__version__ = "0.1.0"
__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

version_info = tuple(int(v) if v.isdigit()
                     else v for v in __version__.split('.'))
