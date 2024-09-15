"""sopel-npm error types

Part of the sopel-npm package.

Copyright 2024 dgw, technobabbl.es
Licensed under the Eiffel Forum License v2
"""
from __future__ import annotations


class NPMError(Exception):
    """Base class for sopel-npm plugin errors."""


class NoResultsError(NPMError):
    """Specific exception type for searching and getting 0 results."""


class PackageNotFoundError(NPMError):
    """Specific exception type for directly looking up a nonexistent package."""
