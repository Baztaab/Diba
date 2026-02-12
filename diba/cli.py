"""
CLI wrapper delegating to diba._cli.app.
"""

from diba._cli.app import dispatch, main
from diba._cli.commands.vedic_d1 import run_vedic_d1_command as run_vedic_d1

__all__ = ["dispatch", "main", "run_vedic_d1"]
