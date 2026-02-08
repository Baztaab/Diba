"""
CLI wrapper delegating to kerykeion._cli.app.
"""

from kerykeion._cli.app import dispatch, main  # noqa: F401
from kerykeion._cli.commands.vedic_d1 import run_vedic_d1_command as run_vedic_d1  # backward compat
