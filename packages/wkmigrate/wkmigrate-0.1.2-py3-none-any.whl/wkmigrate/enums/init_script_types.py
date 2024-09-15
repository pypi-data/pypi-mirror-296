""" Enumeration of supported cluster init script types."""
from enum import Enum


class InitScriptType(Enum):
    DBFS = 'DBFS'
    VOLUMES = 'Volumes'
    WORKSPACE = 'Workspace'
