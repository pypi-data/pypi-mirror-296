"""sopel-npm utilities

Part of the sopel-npm package.

Copyright 2024 dgw, technobabbl.es
Licensed under the Eiffel Forum License v2
"""
from __future__ import annotations


def bytes_to_human(num: int, suffix: str = "B") -> str:
    """Convert ``num`` to a human-friendly scale using binary prefixes.

    Assumes bytes (``suffix="B"``), but this can be overridden.
    """
    # adapted from https://stackoverflow.com/a/1094933/5991
    # using name inspiration from Sopel's `tools.time.seconds_to_human()`
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def format_package_info(info: dict, link: bool = False):
    """Format package ``info`` into a human-friendly message."""
    # Apparently NPM's registry doesn't update the metadata of older packages
    # when schema changes happen, and you just get an older format, potentially
    # with different or omitted fields.
    # I don't particularly like building output this way, but it's easier to
    # read and maintain in the long run over a template string that accounts for
    # all the possible fields that could be missing or nulled in old releases.
    parts = []
    if 'name' in info:
        if 'version' in info:
            parts.append(f"{info['name']}@{info['version']}")
        else:
            parts.append(info['name'])

    # The registry API docs on GitHub[1] show a "publisher" field but I didn't
    # find it in any actual packages I test-fetched. No idea if it's still used,
    # but it's cheap to check for it first.
    # "_npmUser" sounds internal so I kind of hate using it, even though the
    # docs specifically mention it.
    # [1]: https://github.com/npm/registry/blob/main/docs/REGISTRY-API.md
    if 'publisher' in info:
        parts.append("Published by " + info['publisher']['name'])
    elif '_npmUser' in info:
        user = info['_npmUser']
        name = user.get('name') or user.get('username')
        if name:
            parts.append("Published by " + name)

    if 'license' in info:
        parts.append(info['license'] + " license")

    if 'dist' in info and all(
        k in info['dist'] for k in ('unpackedSize', 'fileCount')
    ):
        parts.append(
            "Unpacked size: {} in {} files".format(
                bytes_to_human(info['dist']['unpackedSize']),
                info['dist']['fileCount'],
            )
        )

    if 'description' in info:
        parts.append(info['description'])

    # Notably absent here: when the version was released. Docs (linked above)
    # mention various date/time fields that were simply missing from the live
    # API data when I was writing this, so the "last published" time is simply
    # not implemented. Can't output data you don't have, right?

    trailing = ''  # Sopel requires this to be a string; it can't just be `None`
    if link:
        trailing = ' | ' + 'https://www.npmjs.com/package/{}'.format(info['name'])

    return ' | '.join(parts), trailing
