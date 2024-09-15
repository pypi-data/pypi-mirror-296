"""sopel-npm API functions

Part of the sopel-npm package.

Copyright 2024 dgw, technobabbl.es
Licensed under the Eiffel Forum License v2
"""
from __future__ import annotations

import requests

from sopel.tools import get_logger

from .errors import NPMError, NoResultsError, PackageNotFoundError


LOGGER = get_logger('npm.api')


def fetch_api_endpoint(path: str, params: dict | None = None):
    """Fetch the API endpoint at ``path`` using the given ``params``.

    On error, raises ``.errors.NPMError`` with a message that can be sent to
    IRC in lieu of the expected API results.
    """
    try:
        r = requests.get('https://registry.npmjs.org' + path, params=params)
    except requests.exceptions.ConnectTimeout:
        raise NPMError("Connection timed out.")
    except requests.exceptions.ConnectionError:
        raise NPMError("Couldn't connect to server.")
    except requests.exceptions.ReadTimeout:
        raise NPMError("Server took too long to send data.")
    if r.status_code == 404:
        raise PackageNotFoundError
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        LOGGER.exception("HTTP error talking to NPM API: %r", e)
        raise NPMError("HTTP error: " + e.args[0])
    try:
        data = r.json()
    except ValueError:
        LOGGER.exception("Couldn't decode API response as JSON: %r", r.content)
        raise NPMError("Couldn't decode API response as JSON.")

    return data


def get_package_info(name: str, version: str | None = None):
    """Get information from NPM for the package called ``name``.

    Fetches latest data unless ``version`` is specified.

    Raises ``.errors.NPMError`` on failure, either directly or passed through
    from ``fetch_api_endpoint()``.
    """
    # also want empty-string to trigger this, not just None
    if not version:
        version = 'latest'

    return fetch_api_endpoint('/' + name + '/' + version)


def search_for_package_info(query: str):
    """Search NPM for packages matching the ``query``.

    Returns the first result, according to NPM's sort order.

    Raises ``.errors.NPMError`` on failure, either directly or passed through
    from ``fetch_api_endpoint()``.
    """
    search_parameters = {
        'text': query,
        'size': 1,
    }
    data = fetch_api_endpoint('/-/v1/search', params=search_parameters)

    if not (packages := data.get('objects', [])):
        raise NoResultsError("No search results for '{}'.".format(query))

    # search results contain abbreviated package objects, so we must separately
    # request the package itself
    return get_package_info(packages[0]['package']['name'])
