"""sopel-npm

Sopel plugin to handle NPM links/searches

Copyright 2024 dgw, technobabbl.es
Licensed under the Eiffel Forum License v2
"""
from __future__ import annotations

from sopel import plugin

from .api import get_package_info, search_for_package_info
from .errors import NPMError, NoResultsError, PackageNotFoundError
from .util import format_package_info


PLUGIN_PREFIX = '[npm] '


@plugin.url(
    r'https?://(?:www\.)npmjs\.com/package/'
    r'(?P<package>[^/]+)(?:/v/(?P<version>[^/]+))?/?'
)
@plugin.output_prefix(PLUGIN_PREFIX)
def npm_link(bot, trigger):
    package = trigger.group('package')
    version = trigger.group('version')

    try:
        info = get_package_info(package, version)
        message, trailing = format_package_info(info)
    except PackageNotFoundError:
        bot.reply(
            "No {} '{}{}' found. Are you sure it exists?"
            .format(
                'release' if version else 'package',
                package,
                '@' + version if version else '',
            )
        )
        return
    except NPMError as e:
        bot.reply("Sorry, there was a problem: {}".format(e))
        return

    bot.say(message, truncation=' […]', trailing=trailing)


@plugin.command('npm')
@plugin.output_prefix(PLUGIN_PREFIX)
def npm_search(bot, trigger):
    if not (query := trigger.group(2)):
        bot.reply('What am I supposed to search for?')
        return plugin.NOLIMIT

    try:
        info = search_for_package_info(query)
        message, trailing = format_package_info(info, link=True)
    except NoResultsError as e:
        bot.reply("{}".format(e))
        return
    except NPMError as e:
        bot.reply("Sorry, there was a problem: {}".format(e))
        return

    bot.say(message, truncation=' […]', trailing=trailing)
